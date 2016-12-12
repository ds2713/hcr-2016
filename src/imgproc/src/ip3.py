#!/usr/bin/env python

import rospy

from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Point32

import sensor_msgs.point_cloud2 as pointcloud

import struct

dis_range = 2

noise_lim = 5000

def main():
        rospy.init_node('movement', anonymous=True)
        rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback)
        rospy.spin()

def callback(data):
    pub = rospy.Publisher('follow', Point32, queue_size=1)
    rate = rospy.Rate(10)


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
        str_rgb = struct.pack('f', p[3]).encode('hex')
        print str_rgb

        if p[2] <= dis_range:
        #if p[2] <= dis_range + dis_limit and p[2] >= dis_range - dis_limit:
            xsum = xsum + p[0]
            ysum = ysum + p[1]
            zsum = zsum + p[2]
            num = num + 1

    rate.sleep()

    if num > noise_lim:
		pub.publish(Point32(xsum/num, ysum/num, zsum/num))
    else:
        pub.publish(Point32(0, 0, 0))

if __name__ == '__main__':

    try:
        main()
    except rospy.ROSInterruptException:
        pass
