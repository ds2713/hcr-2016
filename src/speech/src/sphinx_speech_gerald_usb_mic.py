#!/usr/bin/env python

# # NOTE: this example requires PyAudio because it uses the Microphone class

import rospy
import pyaudio
import speech_recognition as sr
from std_msgs.msg import String

index = pyaudio.PyAudio().get_device_count() - 1
print index
print int(index)

keyword_stop = "finish"
keyword_go = "follow"

keywords = [("finish", 0.8), ("follow", 0.8), ("calibrate", 0.8)]

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

    r.dynamic_energy_threshold = True
    r.energy_threshold = 500  # minimum audio energy to consider for recording
    r.pause_threshold = 0.2  # seconds of non-speaking audio before a phrase is considered complete
    r.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
    r.non_speaking_duration = 0.1  # seconds of non-speaking audio to keep on both sides of the recording


    times = 1
    while not rospy.is_shutdown():

        #Open Kinect microphone as audio source
        with sr.Microphone(int(usb_microphone)) as source:

            print("Say something!")
            audio = r.listen(source, phrase_time_limit = 3)

            try:

                try:
                    print("listening")
                    the_output = r.recognize_sphinx(audio, keyword_entries=keywords)
                except sr.UnknownValueError:
                    the_output = "UNKNOWN"
                    rospy.loginfo("Sphinx could not understand audio")
                except sr.RequestError as e:
                    the_output = "REQUEST"
                    rospy.loginfo("Request error; {0}".format(e))

                # if keyword_go in the_output:
                #     keyword_publisher = keyword_go
                #     pub.publish(keyword_publisher)
                # elif keyword_stop in the_output:
                #     keyword_publisher = keyword_stop
                #     pub.publish(keyword_publisher)

                rospy.loginfo(the_output.upper())
                pub.publish(the_output.upper())

            except sr.WaitTimeoutError:
                times = times + 1

if __name__ == '__main__':
    try:
        speechtotext()
    except rospy.ROSInterruptException:
        pass
