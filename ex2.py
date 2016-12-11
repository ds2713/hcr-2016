import pickle
import rospy
from sensor_msgs.msg import PointCloud2

import sensor_msgs.point_cloud2 as pc2
import struct

with open('temp.pickle') as f:  # Python 3: open(..., 'rb')
    thing = pickle.load(f)

for p in pc2.read_points(thing, field_names = ("x", "y", "z", "rgb"), skip_nans=True):
	print " x : %.10f  y: %.10f  z: %.10f " %(p[0],p[1],p[2]) + "rgb: " + struct.pack('f', p[3]).encode('hex')

thing2 = thing.data

# print dir(thing)

# print thing.fields

# print thing.header

# print len(thing2)

x = thing2[0:4]
y = thing2[4:8]
z = thing2[8:12]
empty = thing2[12:16]
rgb = thing2[16:20]
empty2 = thing2[20:32]

print "x"
print [ord(i) for i in x]
b = bytearray()
b.extend(x)
print x

print "y"
print [ord(i) for i in y]
b = bytearray()
b.extend(y)
print b

print "z"
print [ord(i) for i in z]
b = bytearray()
b.extend(z)
print b

print "empty"
print [ord(i) for i in empty]
b = bytearray()
b.extend(empty)
print b

print "rgb"
print [ord(i) for i in rgb]
b = bytearray()
b.extend(rgb)
print b

print "empty2"
print [ord(i) for i in empty2]
b = bytearray()
b.extend(empty2)
print b

