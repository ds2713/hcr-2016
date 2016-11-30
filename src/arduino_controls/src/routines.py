#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16
import serial
import time

def the_routines():
    rospy.init_node('routines', anonymous=True)
    rospy.Subscriber("arduino_routines", Int16, callback)
    rospy.spin()


# 0 is no
# 1 is yes
# 2 is calibrate
# 3 is shake hands
# 4 is change idle
# 5 is play
# 6 is tone

def callback(data):
    PREFIXCALIBRATE = 123
    PREFIXSHAKEHANDS = 111
    PREFIXCHANGEIDLE = 420
    PREFIXYES = 777
    PREFIXNO = 888
    PREFIXPLAY = 999
    PREFIXTONE = 990

    global ser
    case = data.data

    if input_angle != current_head:
        ser.write('{}{}{}'.format(PREFIXHEAD,',',str(input_angle)))
        ser.read(4)
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
        ser.read(4)
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
        ser.read(4)
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
        ser.read(4)
        current_tilt = input_angle
        pub.publish(current_tilt)
    else:
        pass

if __name__ == '__main__':
    global ser
    ser = serial.Serial('/dev/ttyACM0')

    try:
        the_routines()
    except rospy.ROSInterruptException:
        pass
