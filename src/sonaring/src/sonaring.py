#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Point32

import sensor_msgs.point_cloud2 as pointcloud

limit_left = math.pi * 0.75
limit_right = math.pi * 0.25
middle = math.pi * 0.5
dist_limit = 0.5

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
    followy = data.z
    followz = data.y

def avoid(data):
    global followx
    global followy
    global followz

    afollowx = followx
    afollowy = followy
    afollowz = followz

    pub = rospy.Publisher('follow2', Point32, queue_size=10)
    rate = rospy.Rate(10)

    collisions = []

    for p in pointcloud.read_points(data, field_names = ("x", "y", "z"), skip_nans=True):
        x = p[1] * -1
        y = p[0]

        dist = math.hypot(x, y)

        if dist < dist_limit:
            collisions.append([x, y, dist])

    if collisions:
        minimum = [0, 0, dist_limit + 1]

        for each in collisions:
            if each[2] < minimum[2]
                minimum = each

        xcol = minimum[0]
        ycol = minimum[1]

        angle = math.atan2(ycol, xcol)

        if angle => limit_right and angle <= middle:
            cos_angle = math.cos(angle)
            sin_angle = math.sin(angle)

            new_x = cos_angle * afollowx + sin_angle * afollowy
            new_y = cos_angle * afollowy - sin_angle * afollowx

            pub.Publish(Point32(new_x, afollowz, new_y))

        elif angle > middle and angle <= limit_left:
            cos_angle = math.cos(angle - math.pi)
            sin_angle = math.sin(angle - math.pi)

            new_x = cos_angle * afollowx + sin_angle * afollowy
            new_y = cos_angle * afollowy - sin_angle * afollowx

            pub.Publish(Point32(new_x, afollowz, new_y))

        else:
            pub.Publish(Point32(0, 0, 0))

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
