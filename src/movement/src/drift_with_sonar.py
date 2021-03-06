#!/usr/bin/env python
import roslib
import rospy
from geometry_msgs.msg import Twist, Point32
#from std_msgs.msg import Float32
import signal

ur_dis = 1
u_limit = 0.2 # + or - 20cm from the ur_dis
vis_limit = 0.9 #+ or - 20cm from view
speed = 0.5 #speed of motors
speed_back = 0.3
rot_limit = 0.1
rot_speed = 0.3
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

def avoidance(data):
    try:
        velocity_publisher = rospy.Publisher('/RosAria/cmd_vel',Twist, queue_size=10)
        if data.x and data.z and data.y:
            print ("diversion required")
            global diversion
            diversion = True
            if data.z < ur_dis + vis_limit and data.z > ur_dis - vis_limit:
                if data.z > ur_dis + u_limit:
                    #move towards user
                    print "Foward"
                    vel_msg.linear.x = speed
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

            print "Z distance: ", str(data.z)
            print "X distance: ", str(data.x)
            #print str(vel_msg.linear.x)
            velocity_publisher.publish(vel_msg)
        else:
            global diversion
            diversion = False

    except KeyboardInterrupt:
        print "Interrupted"



def callback(data):
    #print str(data)
    try:

        velocity_publisher = rospy.Publisher('/RosAria/cmd_vel',Twist, queue_size=10)

        #while not rospy.is_shutdown():
        if not diversion:
            if data.z < ur_dis + vis_limit and data.z > ur_dis - vis_limit:
                if data.z > ur_dis + u_limit:
                    #move towards user
                    print "Foward"
                    vel_msg.linear.x = speed
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

            print "Z distance: ", str(data.z)
            print "X distance: ", str(data.x)
            #print str(vel_msg.linear.x)
            velocity_publisher.publish(vel_msg)

    except KeyboardInterrupt:
        print "Interrupted"

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/follow", Point32, callback)
    rospy.Subscriber("/follow2", Point32, avoidance)
    rospy.spin()


if __name__ == '__main__':
    global diversion
    diversion = False
    listener()
