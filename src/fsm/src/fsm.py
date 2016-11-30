#!/usr/bin/env python

# 0 is waiting/stop
# 1 is decision
# 2 is go there
# 3 is stay close
# 4 is follow

import rospy
from std_msgs.msg import Int32
from std_msgs.msg import String

def callback(data):
    pub = rospy.Publisher('mode', Int32, queue_size=10)

    inputstring = data.data
    if current_state == 0:
        if "hey" in inputstring:
            new_state = 1
        else:
            new_state = 0
    elif current_state == 1:
        pass
    elif current_state == 2:
        pass
    elif current_state == 3:
        pass
    elif current_state == 4:
        pass
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
