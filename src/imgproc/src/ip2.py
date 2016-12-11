#!/usr/bin/env python

import rospy

from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Point32

import sensor_msgs.point_cloud2 as pointcloud

import struct

def main():
        rospy.init_node('movement', anonymous=True)
        rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback)
        rospy.spin()

def callback(data):
    pub = rospy.Publisher('follow', Point32, queue_size=1)
    rate = rospy.Rate(10)
    dis_range = 1
    dis_limit = 0.2

    xsum = 0
    ysum = 0
    zsum = 0
    num = 0

    for p in pointcloud.read_points(data, field_names = ("x", "y", "z", "rgb"), skip_nans=True):
        # Access each part individually.
        # x = p[0]
        # y = p[1]
        # z = p[2]

        # Deal with later, for RGB, need to convert from String.
        # str_rgb = struct.pack('f', p[3]).encode('hex')

        if num > 76800 :
            pub.publish(Point32(p[0], p[1], p[2]))
            rate.sleep()
            return

        num = num + 1

if __name__ == '__main__':

    try:
        main()
    except rospy.ROSInterruptException:
        pass
