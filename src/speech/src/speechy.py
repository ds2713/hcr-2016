#!/usr/bin/env python

# NOTE: this example requires PyAudio because it uses the Microphone class

import rospy
import speech_recognition as sr
from std_msgs.msg import String


# obtain audio from the microphone
def speechtotext():
    pub = rospy.Publisher('speechinput', String, queue_size=10)
    rospy.init_node('speechy', anonymous=True)
        r = sr.Recognizer()

    r.dynamic_energy_threshold = False
    r.energy_threshold = 500  # minimum audio energy to consider for recording
    r.pause_threshold = 0.2  # seconds of non-speaking audio before a phrase is considered complete
    r.phrase_threshold = 0.3  # minimum seconds of speaking audio before we consider the speaking audio a phrase - values below this are ignored (for filtering out clicks and pops)
    r.non_speaking_duration = 0.1  # seconds of non-speaking audio to keep on both sides of the recording

    times = 1
    while not rospy.is_shutdown():
        with sr.Microphone(sample_rate=32000) as source:
            print "Attempt: " + str(times)
            try:
                audio = r.listen(source, timeout = 1, phrase_time_limit = 3)

                try:
                    the_output = r.recognize_sphinx(audio)
                    the_output = the_output.upper()
                except sr.UnknownValueError:
                    the_output = "UNKNOWN"
                except sr.RequestError as e:
                    the_output = "REQUEST_ERROR"

                rospy.loginfo(the_output)
                pub.publish(the_output)

            except sr.WaitTimeoutError:
                times = times + 1

if __name__ == '__main__':
    try:
        speechtotext()
    except rospy.ROSInterruptException:
        pass
