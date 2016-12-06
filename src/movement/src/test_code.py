#!/usr/bin/env python
import roslib
import rospy
from geometry_msgs.msg import Twist
from time import sleep

ur_dis = 100 # 1 metre user-robot distance
limit = 10 # + or - 10cm from the ur_dis
speed = 5 #speed of motors

def move():
    rospy.init_node('Gerald', anonymous=True)
    velocity_publisher = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size=1)
    vel_msg = Twist()

    #Set the speed of the other parameters to 0

    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    #while not rospy.is_shutdown():
    stop_robot = 0
    # while True:
    #     velocity_publisher.publish(vel_msg)
    #     stop_robot = input("stop robot = ")
    #     if stop_robot != 0:
    #         vel_msg.linear.x = 0
    #         velocity_publisher.publish(vel_msg)
    #         break

    while not rospy.is_shutdown():
    #while True:
        #robot_speed = input("robot_speed = ")
        speed,angle = map(float, raw_input("robot_speed = ").split(' '))

        speed = speed/100
        angle = angle/100

        if speed == 9:
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            velocity_publisher.publish(vel_msg)
            break
        else:
            vel_msg.linear.x = speed
            vel_msg.angular.z = angle

        velocity_publisher.publish(vel_msg)


if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException: pass
