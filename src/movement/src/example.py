#!/usr/bin/env python
import roslib; roslib.load_manifest('head_listener')
import rospy
import tf
import math
from std_msgs.msg import String
from head_pose.msg import head_data
from geometry_msgs.msg import Twist
from tf.transformations import *

def converter(pub,data):
    move = Twist()
    if (data.pitch > 0.15) and (data.pitch < 1.0): #looking down
        move.linear.x = 0.5
    elif (data.pitch < -0.4) and (data.pitch > -1.0): #looking up
        move.linear.x = -0.5
    elif (data.yaw > 0.4) and (data.yaw < 1.0): #looking left
        move.angular.z = 0.5
    elif (data.yaw < -0.4) and (data.yaw > -1.0): #looking right
        move.angular.z = -0.5
    else:
        move.linear.x = 0.0
        move.angular.z = 0.0
    print(move)
    pub.publish(move)


def callback(data):
    pub = rospy.Publisher('cmd_vel',Twist)
    converter(pub,data)
    head_tf = tf.TransformBroadcaster()
    # quaternion = quaternion_from_euler(data.roll,data.pitch,data.yaw)
    #(data.x_center/1000.0,data.y_center/1000.0,data.z_center/1000.0)
    head_tf.sendTransform((data.x_center/1000.0,-data.y_center/1000.0,data.z_center/1000.0),
        quaternion_from_euler(0,data.pitch,math.pi+data.yaw), #roll,pitch,yaw
        rospy.Time.now(),
        "head_pose",
        "xtion")
    #rospy.loginfo("Time to move!")
    #print(data)


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("Head_Pose_Data", head_data, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()