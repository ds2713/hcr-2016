#!/usr/bin/env python

# 0 is stop
# 1 is go

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String

def callback(data):
    inputstring = data.data

    global current_state
    new_state = 0

    pub = rospy.Publisher('mode', Int32, queue_size=10)

    if current_state == 0:
        if "GO" in inputstring:
            new_state = 1
        else:
            new_state = 0

    elif current_state == 1:
        if "STOP" in inputstring:
            new_state = 0
        else:
            new_state = 1

    else:
        new_state = 0

    pub.publish(new_state)
    current_state = new_state

def listener():
    rospy.init_node('states', anonymous=True)
    rospy.Subscriber("speechinput", String, callback)
    rospy.spin()

if __name__ == '__main__':
    global current_state
    current_state = 0
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
