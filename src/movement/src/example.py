#!/usr/bin/env python
import roslib
import rospy
from geometry_msgs.msg import Twist, Point32
#from std_msgs.msg import Float32
import signal

ur_dis = 1
limit = 0.2 # + or - 10cm from the ur_dis
limit2 = 0.9
speed = 0.5 #speed of motors
max_dis = 2

vel_msg = Twist()

#Set the speed of the other parameters to 0
#vel_msg.linear.x = 0
vel_msg.linear.y = 0
vel_msg.linear.z = 0
vel_msg.angular.x = 0
vel_msg.angular.y = 0
vel_msg.angular.z = 0

def sigint_handler(signum, frame):
    print "Interrupted"
    # rospy.init_node('killer', anonymous=True)
    velocity_publisher = rospy.Publisher('/RosAria/cmd_vel',Twist, queue_size=10)
    vel_msg.linear.x = 0
    vel_msg.angular.z = 0
    while not rospy.is_shutdown():
        velocity_publisher.publish(vel_msg)

signal.signal(signal.SIGINT, sigint_handler)

def callback(data):
    #print str(data)
    try:

        velocity_publisher = rospy.Publisher('/RosAria/cmd_vel',Twist, queue_size=10)

        #while not rospy.is_shutdown():
        if data.z < ur_dis + limit2 and data.z > ur_dis - limit2:
        	if data.z > ur_dis + limit:
        		#move towards user
        		vel_msg.linear.x = speed
                #print ("Forward")
        	elif data.z < ur_dis - limit:
        		#move away from user
        		vel_msg.linear.x = -speed
                #print "Backward"
        	else:
        		#stop, in good distance from user
        		vel_msg.linear.x = 0
                #print "Stop"


        else:
        	#outside of expected range
        	vel_msg.linear.x = 0

        print str(data.z)
        #print str(vel_msg.linear.x)
        velocity_publisher.publish(vel_msg)

    except KeyboardInterrupt:
        print "Interrupted"


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/follow", Point32, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
