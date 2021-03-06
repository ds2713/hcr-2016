#!/usr/bin/env python

# # NOTE: this example requires PyAudio because it uses the Microphone class

import rospy
import pyaudio
import speech_recognition as sr
from std_msgs.msg import String

index = pyaudio.PyAudio().get_device_count() - 1
print index
print int(index)

keyword_stop = "stay"
keyword_go = "follow"

#Device name for Kinect audio device
search_word = "Kinect USB Audio"

#Open pyaudio functions to listen to audio devices
p = pyaudio.PyAudio

#Search through all available audio devices to find Kinect
for i in range (0, index):
    details = str(pyaudio.PyAudio().get_device_info_by_index(i))
    #If Kinect is found, remember which device it is!
    if search_word in details:
        # print details
        usb_microphone = i
        print "Found USB device. Device: ", usb_microphone

# print usb_microphone

# obtain audio from the microphone
def speechtotext():
    pub = rospy.Publisher('speechinput', String, queue_size=10)
    rospy.init_node('speechy', anonymous=True)

    r = sr.Recognizer()

    times = 1
    while not rospy.is_shutdown():

        #Open Kinect microphone as audio source
        with sr.Microphone(int(usb_microphone)) as source:

            print("Say something!")
            audio = r.listen(source)

            try:

                try:
                    print("listening")
                    the_output = r.recognize_google(audio)
                except sr.UnknownValueError:
                    the_output = "Sorry, I couldn't understand you"
                    rospy.loginfo("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    the_output = "Sorry, I couldn't understand you"
                    rospy.loginfo("Could not request results from Google Speech Recognition service; {0}".format(e))

                if keyword_go in the_output:
                    keyword_publisher = keyword_go
                    pub.publish(keyword_publisher)
                elif keyword_stop in the_output:
                    keyword_publisher = keyword_stop
                    pub.publish(keyword_publisher)

                rospy.loginfo(the_output)

            except sr.WaitTimeoutError:
                times = times + 1

if __name__ == '__main__':
    try:
        speechtotext()
    except rospy.ROSInterruptException:
        pass
