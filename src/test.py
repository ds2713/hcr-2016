#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2

def main():
        rospy.init_node('movement', anonymous=True)
        rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback)
        rospy.spin()

def callback(data):
    with open('temp.pickle', 'w') as f:  # Python 3: open(..., 'wb')
        pickle.dump(data, f)

if __name__ == '__main__':

    try:
        update()
    except rospy.ROSInterruptException:
        pass
