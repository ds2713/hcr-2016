#!/usr/bin/env python

# 0 is waiting/stop
# 1 is decision
# 2 is go there
# 3 is stay close
# 4 is follow

import rospy
from std_msgs.msg import String

def callback(data):
    inputstring = data.data
    if current_state == 0:
        pass
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
