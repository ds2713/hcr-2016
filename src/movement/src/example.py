#!/usr/bin/env python
import roslib
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

ur_dis = 1.5
limit = 0.1 # + or - 10cm from the ur_dis
speed = 1 #speed of motors
max_dis = 4

def callback(data):
    #print str(data)

    velocity_publisher = rospy.Publisher('/RosAria/cmd_vel',Twist, queue_size=10)

    vel_msg = Twist()

    #Set the speed of the other parameters to 0
    #vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    #while not rospy.is_shutdown():
    if data.data < max_dis:
    	if data.data > ur_dis + limit:
    		#move towards user
    		vel_msg.linear.x = speed
    	elif data.data < ur_dis - limit:
    		#move away from user
    		vel_msg.linear.x = -speed
    	else:
    		#stop, in good distance from user
    		vel_msg.linear.x = 0
    else:
    	#outside of expected range
    	vel_msg.linear.x = 0

    print str(data.data)
    velocity_publisher.publish(vel_msg)


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/dis_topic", Float32, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
