#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import serial
import time

def update():
    rospy.init_node('arduino_update', anonymous=True)
    rospy.Subscriber("headangle_in", Float32, callback_headangle)
    rospy.Subscriber("clawdist_in", Float32, callback_clawdist)
    rospy.Subscriber("liftdist_in", Float32, callback_liftdist)
    rospy.Subscriber("tiltangle_in", Float32, callback_tiltangle)
    rospy.spin()

def callback_headangle(data):
    global ser
    global PREFIXHEAD
    global current_head

    pub = rospy.Publisher('headangle_out', Float32, queue_size=10)
    input_angle = data.data
    if input_angle != current_head:
        ser.write('{}{}{}'.format(PREFIXHEAD,',',str(input_angle)))
        ser.read(1)
        current_head = input_angle
        pub.publish(current_head)
    else:
        pass

def callback_clawdist(data):
    global ser
    global PREFIXCLAW
    global current_claw

    pub = rospy.Publisher('clawdist_out', Float32, queue_size=10)
    input_distance = data.data
    if input_distance != current_claw:
        ser.write('{}{}{}'.format(PREFIXCLAW,',',str(input_distance)))
        ser.read(1)
        current_claw = input_distance
        pub.publish(current_claw)
    else:
        pass

def callback_liftdist(data):
    global ser
    global PREFIXLIFT
    global current_lift

    pub = rospy.Publisher('liftdist_out', Float32, queue_size=10)
    input_distance = data.data
    if input_distance != current_lift:
        ser.write('{}{}{}'.format(PREFIXLIFT,',',str(input_distance)))
        ser.read(1)
        current_lift = input_distance
        pub.publish(current_lift)
    else:
        pass

def callback_tiltangle(data):
    global ser
    global PREFIXTILT
    global current_tilt

    pub = rospy.Publisher('tiltangle_out', Float32, queue_size=10)
    input_angle = data.data
    if input_angle != current_tilt:
        ser.write('{}{}{}'.format(PREFIXTILT,',',str(input_angle)))
        ser.read(1)
        current_tilt = input_angle
        pub.publish(current_tilt)
    else:
        pass

if __name__ == '__main__':
    global ser
    ser = serial.Serial('/dev/ttyACM0', timeout=10.0)

    global PREFIXHEAD
    PREFIXHEAD = '666'
    global PREFIXCLAW
    PREFIXCLAW = '555'
    global PREFIXLIFT
    PREFIXLIFT = '444'
    global PREFIXTILT
    PREFIXTILT = '333'

    global current_head
    global current_claw
    global current_lift
    global current_tilt
    current_head = 0
    current_claw = 0
    current_lift = 0
    current_tilt = 0

    ser.write('{}{}{}'.format(PREFIXHEAD,',',str(0)))     # write a string
    ser.write('{}{}{}'.format(PREFIXCLAW,',',str(0)))
    ser.write('{}{}{}'.format(PREFIXLIFT,',',str(0)))
    ser.write('{}{}{}'.format(PREFIXTILT,',',str(0)))

    try:
        update()
    except rospy.ROSInterruptException:
        pass
