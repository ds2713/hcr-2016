#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Point32
import math

import sensor_msgs.point_cloud2 as pointcloud

middle = math.pi * 0.5
dist_limit = 0.75

def main():
    rospy.init_node('sonary', anonymous=True)
    rospy.Subscriber('/follow', Point32, callback)
    rospy.Subscriber('/RosAria/sonar_pointcloud2', PointCloud2, avoid)
    rospy.spin()

def callback(data):
    global followx
    global followy
    global followz

    followx = data.x
    followy = data.y
    followz = data.z

def avoid(data):
    global followx
    global followy
    global followz

    pub = rospy.Publisher('follow2', Point32, queue_size=10)
    rate = rospy.Rate(2)

    collisions = []

    for p in pointcloud.read_points(data, field_names = ("x", "y", "z"), skip_nans=True):
        x = p[1] * -1
        y = p[0]

        dist = math.hypot(x, y)

        if y > 0 and abs(x) <= y and dist < dist_limit:
            collisions.append([x, y, dist])

    if collisions:
        minimum = [0, 0, dist_limit + 1]

        for each in collisions:
            if each[2] < minimum[2]:
                minimum = each

        xcol = minimum[0]
        ycol = minimum[1]

        angle = math.atan2(ycol, xcol)

        if angle <= middle:
            cos_angle = math.cos(angle)
            sin_angle = math.sin(angle)

            new_x = cos_angle * followx - sin_angle * followy
            new_z = cos_angle * followy + sin_angle * followx

            pub.publish(Point32(new_x, followy, new_z))

        elif angle > middle:
            cos_angle = math.cos(angle - math.pi)
            sin_angle = math.sin(angle - math.pi)

            new_x = cos_angle * followx - sin_angle * followy
            new_z = cos_angle * followy + sin_angle * followx

            pub.publish(Point32(new_x, followy, new_z))

        else:
            pub.publish(Point32(0, 0, 0))
    else:
        pub.publish(Point32(0, 0, 0))

    rate.sleep()

if __name__ == '__main__':
    global followx
    global followy
    global followz

    followx = 0
    followy = 0
    followz = 0

    try:
        main()
    except rospy.ROSInterruptException:
        pass
