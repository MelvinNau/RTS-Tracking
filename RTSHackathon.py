import numpy as np
import cv2
import requests
import sys
import time

V_CENTER = 130;
V_MARGIN_L = 110;
V_MARGIN_H = 150;

H_CENTER = 400;
H_MARGIN_L = 420;
H_MARGIN_H = 380;


def tallyCommand(url):
    r = requests.get("http://" + url + "/cgi-bin/aw_ptz?cmd=%23DA&res=1")
    print(r.text)

    if r.status_code == 200:
        if r.text == "dA0":
            return True
        else:
            return False
    else:
        print("Error in tallyCommand")
        return False

def tiltCommand(url, speed, movement):
    if tallyCommand(url):
        r = requests.get("http://" + url + "/cgi-bin/aw_ptz?cmd=%23" + movement + str(int(speed)) + "&res=1")
        if r.status_code == 200:
            print("move")
        else:
            print("Error in tiltCommand with speed", speed)

def detect(path, url):
    url = "http://"+ url + "/cgi-bin/mjpeg?resolution=640x360&framerate=25&quality=1"
    autoPilot = True
    scale_factor = 1.2
    min_neighbors = 3
    min_size = (50, 50)

    cascade = cv2.CascadeClassifier(path)
    video_cap = cv2.VideoCapture(url)
    loadHaarcascade = cascade.load(path)
    if not loadHaarcascade:
        print("Check your path for haar cascade file")
        return
    while True:
        while autoPilot:
            ret, img = video_cap.read()

            if ret == False:
                print("Problem in url")
                return
            else:
                print("Autopilot activate")

            #converting to gray image for faster video processing
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            rects = cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size)

            # If at least 1 face detected
            if len(rects) >= 0:
                # Draw a rectangle around the faces
                for (x, y, w, h) in rects:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    print(w)
                    if w >= 100:
                        print("Plan serré")
                    else:
                        print("Plan large")

                    v_delta = V_CENTER - y
                    if (v_delta < 0):
                        v_delta *= -1;

                    if (v_delta > 20):
                        v_delta = 20

                    v_delta /= 2

                    # "T" for up/down
                    if (y < V_MARGIN_L):
                        tiltCommand(url, 50 + v_delta, "T")

                    # "P" for left/right
                    # if (x < H_MARGIN_L):
                    #     tiltCommand(url, 50 - v_delta, "P")

                    if (y > V_MARGIN_L and y < V_MARGIN_H):
                        tiltCommand(url,50, "T")

                    # if (x > H_MARGIN_L and x < H_MARGIN_H):
                        # tiltCommand(url,50, "P")

                    if (y > V_MARGIN_H):
                        tiltCommand(url,50 - v_delta, "T")

                    # if (x > H_MARGIN_H):
                    #     tiltCommand(url,50 + v_delta, "P")

                    print(v_delta)

                # Display the resulting frame
                cv2.imshow('RTS Hachaton', img)
                if cv2.waitKey(10) & 0xFF == ord('a'):
                    autoPilot = False
                    tiltCommand(url, 50, "T")
                elif cv2.waitKey(10) & 0xFF == ord('w'):
                    video_cap.release()
                    sys.exit(0)


        # Use function to pilot with 'z' to up and 's' to down
        while not autoPilot:
            ret, img = video_cap.read()

            if ret == False:
                print("Problem in url")
                return
            else:
                print("Autopilot deactivate")

            #converting to gray image for faster video processing
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            rects = cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=min_neighbors, minSize=min_size)

            # If at least 1 face detected
            if len(rects) >= 0:
                # Draw a rectangle around the faces
                for (x, y, w, h) in rects:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    print(w)
                    if w >= 100:
                        print("Plan serré")
                    else:
                        print("Plan large")
                cv2.imshow('RTS Hachaton', img)

                if cv2.waitKey(1) & 0xFF == ord('a'):
                    autoPilot = True
                    print("autopilot true")
                    break
                elif cv2.waitKey(10) & 0xFF == ord('z'):
                    tiltCommand(url, 70, "T")
                    time.sleep(0.2)
                    tiltCommand(url, 50, "T")
                elif cv2.waitKey(10) & 0xFF == ord('s'):
                    tiltCommand(url, 30, "T")
                    time.sleep(0.2)
                    tiltCommand(url, 50, "T")
                elif cv2.waitKey(10) & 0xFF == ord('w'):
                    video_cap.release()
                    sys.exit(0)

    video_cap.release()

def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "100.100.100.100"
    print(url)
    cascadeFilePath="./haarcascade_frontalface_default.xml"

    detect(cascadeFilePath, url)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
