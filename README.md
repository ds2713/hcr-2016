# Human Centred Robotics 2016 (hcr-2016)
Repository for HCR coursework for Gerald, the Shopping Assistant Robotics

## Summary ##
This repository contains the files used for the development and testing of our robot, Gerald. At this level, there are two important folders to note.
1. The `HCR_robot_movement` folder contains the program for the Arduino that was controlling the gripper and camera movement.
2. `src` is the folder that contains all the packages that were used.

## Things inside `src ` that are ours ##

1. `arduino controls` - The Arduino controls are here.
  * `arduino.py` and `arduino2.py` are for the two possible serial port outputs that would need to be opened, depending on how the Arduino connected. This node listened to 4 different topics, for the head angle, the head tilt, the gripper height, and the gripper claw. It then sent the appropriate serial data, before publishing to a corresponding topic the new angle.
  * `routines.py` listens to a topic, and depending on the value, would send commands to the Arduino to perform certain preprogrammed routines, like nodding, or calibration.

2. `fsm` - The finite state machine
  * `fsm.py` was originally designed to listen to the speech output, before outputting to a topic the mode of either following, or note. Ultimately, this functionality was moved into the movement node itself, and this was never used.

3. `imgproc` - The computer vision part.
  * `ip_backup.py` is a backup of `ip.py`
  * `ip.py` was the first iteration of the computer vision node. It reads in the depth cloud from the Kinect's nodes and outputs a Point32 of the most likely position of a human to follow. `ip2.py` contains some tweaks to the calibration parameters, such as distance and noise limit.
  * `ip3.py` is the node that in addition to the depth cloud processing for the average point, also includes a colour hystersis element to ensure that subsequent points published are only done so if the average RGB values are similar. This also listens to the speech output for calibration to reset the colour profile.

4. `movement` - The nodes for movement modes.

5. `shopper` - Only contains launch files.
  * `launch.launch` contains the final combination of all the nodes. The only thing commented out is the sonar, which was seen to be unreliable, and could even interfere with the speech recognition.
  * `launch2.launch` is the one used for the testing with subjects. The Arduino nodes are left out, and while the speech node is up, the processing node is depth only (no RGB) and the following system is simplified to prevent unpredictable behaviour during a test.
  * `launch3.launch` is an example of the setup for the unused `openni_tracker` package. The configuration allows the frames from the camera to match the robots and allows the skeletal tracking to be displayed superimposed onto RGB frames.

6. `sonaring` - The sonar node
  * `sonaring.py`, although not ultimately used, contains the processing for the sonar depth cloud. It would subscribe to the following point from the `imgproc` node in use, then rotate it if necessary to avoid an obstacle, before publishing to another topic.

7. `speech` - Speech processing
  * `speechy.py` was the original speech recognition node using Sphinx that was not as optimised as it could it. It was linked to the laptop's mic and was trying to convert all speech to text. It did not perform well.
  * `google_speech_gerald_usb_mic.py` was an attempt at using the Google Speech-to-Text API with a USB mic that we borrowed. While Google is good, there are limits to the free service, in the form of the maximum number of requests per day. This is very much what `google_speech.py` and `google_speech_gerald.py` do.
  * `sphinx_speech_gerald_usb_mic.py` is the final one. Still using Sphinx, it was tailored to use the Kinect's USB microphones, which allowed a much better performance since those microphones actually face the speaker. Additionally, the Sphinx part was modified to look out for only certain words. This increased its accuracy for those words dramatically, and this is the final node used for our robot.

## Things inside `src` that are not ours ##
In other words, these were repositories that were cloned here from Github as part of our project.

1. `openni_camera`
  * Taken directly from the Github repo, this is where all the nodes that interact with the Kinect live. Not really used ever, as the only interaction is with `openni_launch`, which calls the relevant scripts here.

2. `openni_launch`
  * The part of `openni` that is actually used. This contains a launch file and initialises the Kinect and allows its data to be published to the topics in ROS. That file is `openni.launch`.

3. `openni_tracker`
  * The defunct tracker that used to work in conjunction with ROS and the other `openni` nodes. Unfortunately, it does not work when the platform is moving. It was left here after that.

4. `rosaria`
  * This is the package that interacts with the robot! When run, it listens for movement data, and it also publishes the sonar, and other sensor data. The

5. `rosaria_client`
  * A teleoperating client used to test out the RosAria configuration at the start.
