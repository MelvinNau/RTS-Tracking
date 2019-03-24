# RTS Hackathon
## Tracking face and autopilot for AW-HE2 Series camera

### Goal of the project
The goal was to track the face of a person to adapt the vertical position of the camera during the non recorder sequences.

### Requirements to use
* Python3   
* Numpy   
 * `python3 -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose`
* OpenCV
 * `pip install opencv-python`       
* Requests
 * `python3 -m pip install`

### Utilisation in terminal
* `python3 RTSHackaton.py` without argument use 100.100.100.100 address
* `python3 RTSHackaton.py 100.200.300.400` with argument to use another camera

### Main features     
When the project is start you can:  
* Press **a** key to activate or deactivate the **autoPilot** mode.  
* When you are in **normal** mode, you can press **z** to bring up the camera, or press **s** to go down.
* To quit the program, you can press **w**
