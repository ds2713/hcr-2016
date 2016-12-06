#!/usr/bin/env python
import roslib
import rospy
from std_msgs.msg import Float32
from time import sleep

def talker():
    rospy.init_node('dis_node', anonymous=True)
    pub = rospy.Publisher('dis_topic', Float32, queue_size=1)

    distance = [3, 2.8, 2.6, 2.4, 2, 1, 3, 3.2, 3.4]

    for x in range (0,5):
        for dis in distance:
            sleep(5)
            pub.publish(dis)

    # while True:
    #     sleep(1)
    #     pub.publish(distance[i])

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
