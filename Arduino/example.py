import serial
import time

ser = serial.Serial('/dev/ttyACM0')  # open serial port
PREFIXHEAD = '666'
PREFIXCLAW = '555'
PREFIXLIFT = '444'
PREFIXTILT = '333'


print(ser.name)         # check which port was really used


ser.write('{}{}{}'.format(PREFIX,',',str(headangle)))     # write a string
ser.write('{}{}{}'.format(PREFIX,',',str(clawdist)))
ser.write('{}{}{}'.format(PREFIX,',',str(liftdist)))
ser.write('{}{}{}'.format(PREFIX,',',str(tiltangle)))

ser.close()
