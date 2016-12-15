#!/usr/bin/env python
import roslib
import rospy
from math import sqrt, sin, cos, radians
from geometry_msgs.msg import Twist, Point32
from std_msgs.msg import Float32
#from std_msgs.msg import Float32
import signal

ur_dis = 1
z_limit = 1
u_limit = 0.2 # + or - from the ur_dis
vis_limit = 0.9 #+ or - from view
speed = 0.2 #speed of motors
speed_back = 0.3
rot = 0.1
rot_limit = 0;
rot_speed = 0.3
max_dis = 2
global angle
angle = 0
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

        dis = sqrt(data.z**2 + data.x**2)
        #deviation = dis - ur_dis
        global angle

        x_prime = data.x * cos(angle) - data.z * sin(angle)
        z_prime = data.x * sin(angle) + data.z * cos(angle)

        ur_dis_prime = ur_dis * cos(angle) - rot * sin(angle)
        rot_prime = ur_dis * sin(angle) + rot * cos(angle)

        u_limit_prime = u_limit * cos(angle) - rot * sin(angle)
        rot_limit_prime = u_limit * sin(angle) + rot * cos(angle)

        print "u_limit prime: " + str(u_limit_prime)
        #while not rospy.is_shutdown():
        if dis > 0:
            if z_prime > ur_dis_prime + u_limit_prime:
                #move towards user
                print "Forward"
                #rospy.loginfo("Forward")
                vel_msg.linear.x = speed * (dis/ur_dis)
                #vel_msg.angular.z = speed * sin(angle) + rot_speed * cos(angle)
                #print ("Forward")
            elif z_prime < ur_dis_prime - u_limit_prime:
                #move away from user
                print "Backward"
                #rospy.loginfo("Backward")
                vel_msg.linear.x = -speed_back
                #vel_msg.angular.z = -(speed * sin(angle) + rot_speed * cos(angle))
                #print "Backward"
            else:
                #stop, in good distance from user
                print "Stop"
                #rospy.loginfo("Stop")
                vel_msg.linear.x = 0
                #print "Stop"

        else:
            #outside of expected range
            print "Stop blind"
            #rospy.loginfo("Stop blind")
            vel_msg.angular.z = 0
            print "straight blind"
            #rospy.loginfo("straight blind")
            vel_msg.linear.x = 0

        print "Z distance: " + str(data.z)
        #rospy.loginfo("Z distance: " + str(data.z))
        print "X distance: " + str(data.x)
        #rospy.loginfo("X distance: " + str(data.x))
        print "dis: " + str(dis)
        #rospy.loginfo("dis: " + str(dis))
        #print "deviation: ", str(deviation)
        print "z prime: " + str(z_prime)
        #rospy.loginfo("z prime: " + str(z_prime))
        print "x_prime: " + str(x_prime)
        #rospy.loginfo("x_prime: " + str(x_prime))
        #print str(vel_msg.linear.x)
        velocity_publisher.publish(vel_msg)

    except KeyboardInterrupt:
        rospy.loginfo("Interrupted")

def head_angle(data):
    global angle
    print "angle = " + str(angle)
    angle = radians(data)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/follow", Point32, callback)
    rospy.Subscriber("headangle_out", Float32, head_angle)
    rospy.spin()


if __name__ == '__main__':
    listener()
