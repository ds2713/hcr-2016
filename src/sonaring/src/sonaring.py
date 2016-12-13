#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Point32

import sensor_msgs.point_cloud2 as pointcloud

def main():
    rospy.init_node('sonary', anonymous=True)
    rospy.Subscriber('/follow', Point32, callback)
    rospy.Subscriber('/RosAria/sonar_pointcloud2', PointCloud2, avoid)
    rospy.spin()

def callback(data):
    global followx
    global followy

    followx = data.x
    followy = data.z

def avoid(data):
    global followx
    global followy

    afollowx = followx
    afollowy = followy

    pub = rospy.Publisher('follow2', Point32, queue_size=10)
    rate = rospy.Rate(10)

    count = 0
    for p in pointcloud.read_points(data, field_names = ("x", "y", "z"), skip_nans=True):
        x = p[0]
        y = p[1]
        if count == 3:
            print "x ", x
            print "y ", y
        count = count + 1
    rate.sleep()




if __name__ == '__main__':
    global followx
    global followy

    followx = 0
    followy = 0

    try:
        main()
    except rospy.ROSInterruptException:
        pass
