#!/usr/bin/env python

import rospy

from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Point32
import math

import sensor_msgs.point_cloud2 as pointcloud

import struct

dis_range = 2
noise_lim = 5000
limit_rgb = 15
limit_blob = .25

def main():
        rospy.init_node('movement', anonymous=True)
        rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback)
        rospy.Subscriber("speechinput", String, mode)
        rospy.spin()

def mode(data):
    global start

    if "CALIBRATE" in data.data:
        start = True
    else:
        start = False

def callback(data):
    global old_rgb
    global old_blob
    global start

    pub = rospy.Publisher('follow', Point32, queue_size=1)
    rate = rospy.Rate(10)

    xsum = 0
    ysum = 0
    zsum = 0

    rsum = 0
    gsum = 0
    bsum = 0

    num = 0

    for p in pointcloud.read_points(data, field_names = ("x", "y", "z", "rgb"), skip_nans=True):
        # Access each part individually.
        # x = p[0]
        # y = p[1]
        # z = p[2]

        # Deal with later, for RGB, need to convert from String.
        # rrggbbXX
        str_rgb = struct.pack('f', p[3]).encode('hex')
        # r = int(str_rgb[0:2])
        # g = int(str_rgb[2:4])
        # b = int(str_rgb[4:6])

        if p[2] <= dis_range:
        #if p[2] <= dis_range + dis_limit and p[2] >= dis_range - dis_limit:
            xsum = xsum + p[0]
            ysum = ysum + p[1]
            zsum = zsum + p[2]

            rsum = rsum + int(str_rgb[0:2], 16)
            gsum = gsum + int(str_rgb[2:4], 16)
            bsum = bsum + int(str_rgb[4:6], 16)

            num = num + 1

    if num > noise_lim:
        new_blob = [xsum/num, ysum/num, zsum/num]
        new_rgb = [rsum/num, gsum/num, bsum/num]

        diff_rgb = [new_rgb[0] - old_rgb[0], new_rgb[1] - old_rgb[1], new_rgb[2] - old_rgb[2]]
        mag_diff_rgb = math.sqrt(diff_rgb[0] * diff_rgb[0] + diff_rgb[1] * diff_rgb[1] + diff_rgb[2] * diff_rgb[2])
        # diff_blob = [new_blob[0] - old_blob[0], new_blob[1] - old_blob[1], new_blob[2] - old_blob[2])]
        # mag_diff_blob = math.sqrt(diff_blob[0] * diff_blob[0] + diff_blob[1] * diff_blob[1] + diff_blob[2] * diff_blob[2])

        if start:
            pub.publish(Point32(new_blob[0], new_blob[1], new_blob[2]))
            # old_blob = new_blob
            old_rgb = new_rgb
            start = False

        # elif mag_diff_blob < limit_blob and mag_diff_rgb < limit_rgb:
        elif mag_diff_rgb < limit_rgb:
            pub.publish(Point32(new_blob[0], new_blob[1], new_blob[2]))
            # old_blob = new_blob
            old_rgb = new_rgb

        else:
            pub.publish(Point32(0, 0, 0))

    else:
        pub.publish(Point32(0, 0, 0))

    rate.sleep()

if __name__ == '__main__':
    global old_blob
    global old_rgb
    old_blob = [0, 0, 0]
    old_rgb = [0, 0, 0]

    global start
    start = False

    try:
        main()
    except rospy.ROSInterruptException:
        pass
