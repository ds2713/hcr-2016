import serial
import time

ser = serial.Serial('/dev/ttyACM0')  # open serial port
PREFIX = '666'
angle = 50.0
speed = 50.0 		# degrees per second
delay = 1.0 + angle/speed
print(ser.name)         # check which port was really used

for x in range (0,1):
	print(delay)
	print('Forwards ' + str(angle) + ' degrees')
	ser.write('{}{}{}{}'.format(PREFIX,',','+',str(angle)))     # write a string
	time.sleep(delay)
	print('Backwards ' + str(angle) + ' degrees')
	ser.write('{}{}{}{}'.format(PREFIX,',','-',str(angle)))
	time.sleep(delay)

ser.close()
