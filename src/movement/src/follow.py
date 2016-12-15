#!/usr/bin/env python

import roslib
import rospy
from geometry_msgs.msg import Twist, Point32
from std_msgs.msg import String
from std_msgs.msg import Float32
import signal
import math

ur_dis = 1
u_limit = 0.2 # + or - 20cm from the ur_dis
vis_limit = 0.9 #+ or - 20cm from view
speed = 0.3 #speed of motors
speed_back = 0.3
rot_limit = 0.2
rot_speed = 0.3
max_dis = 2

keyword_stop = "FINISH"
keyword_go = "FOLLOW"

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
    global follow
    print follow
    try:

        velocity_publisher = rospy.Publisher('/RosAria/cmd_vel',Twist, queue_size=10)

        if follow == True:
            print "Should be following"
            #while not rospy.is_shutdown():
            dis = math.sqrt(data.z**2 + data.x**2)

            if dis > 0:
                if data.z > ur_dis + u_limit:
                    #move towards user
                    print "Forward"
                    vel_msg.linear.x = speed * (dis/ur_dis)
                    #print ("Forward")
                elif data.z < ur_dis - u_limit:
                    #move away from user
                    print "Backward"
                    vel_msg.linear.x = -speed_back
                    #print "Backward"
                else:
                    #stop, in good distance from user
                    print "Stop"
                    vel_msg.linear.x = 0
                    #print "Stop"

                if data.x < rot_limit:
                    #move towards user
                    print "Right"
                    vel_msg.angular.z = rot_speed
                    #print ("Forward")
                elif data.x > rot_limit:
                    #move away from user
                    print "Left"
                    vel_msg.angular.z = -rot_speed
                    #print "Backward"
                else:
                    #stop, in good distance from user
                    print "Straight"
                    vel_msg.angular.z = 0
                    #print "Stop"
            else:
                #outside of expected range
                print "Stop blind"
                vel_msg.angular.z = 0
                print "straight blind"
                vel_msg.linear.x = 0
        else:
            print("Not meant to be following!")
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0

        #print str(data.z)
        #print str(vel_msg.linear.x)
        velocity_publisher.publish(vel_msg)

    except KeyboardInterrupt:
        print "Interrupted"

def follow_command(data):

    beep_publisher = rospy.Publisher('beep',Float32, queue_size=10)

    print("Follow commanded")

    global follow

    if keyword_stop in data.data:
        follow = False
        print("Stopping")
        beep_publisher.publish(2)

    elif keyword_go in data.data:
        follow = True
        print("Following")
        beep_publisher.publish(3)
        print follow


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/follow", Point32, callback)
    rospy.Subscriber("/speechinput", String, follow_command)
    rospy.spin()

if __name__ == '__main__':
    print "Follow function running"
    global follow
    follow = False
    listener()
