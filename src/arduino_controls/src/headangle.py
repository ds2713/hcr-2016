#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16

def update_headangle():
    global pub = rospy.Publisher('headangle_in', String, queue_size=10)
    rospy.init_node('headangle', anonymous=True)
    rospy.Subscriber("speechinput", String, callback)
    rospy.spin()


                rospy.loginfo(the_output)
                pub.publish(the_output)

            except sr.WaitTimeoutError:
                times = times + 1

if __name__ == '__main__':
    try:
        update_headangle()
    except rospy.ROSInterruptException:
        pass
