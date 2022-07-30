# for hint

COLORS = {'blue': (255, 0, 0), 'green': (0, 255, 0), 'red': (0, 0, 255), 'yellow':
(0, 255, 255), 'magenta': (255, 0, 255), 'cyan': (255, 255, 0), 'white': (255, 255,
255), 'amber': (255, 191, 0), 'gray': (125, 125, 125), 'dark_gray': (50, 50, 50),
'light_gray': (220, 220,220), 'black': (0,0,0)}

#radius of the clock
RADIUS = 260

#Center point of the clock
CENTER = (320,320)

#The total size of background
CANVAS_SIZE = (640,640,3)




# functions
import cv2
import datetime
import math

#import the attributes
from constants import COLORS
from constants import RADIUS
from constants import CENTER


#get theposition of ticks from the function
def get_ticks():
	hours_init = []
	hours_dest = []

	for i in range(0,360,6):
		x_coordinate = int(CENTER[0] + RADIUS * math.cos(i * math.pi / 180))
		y_coordinate = int(CENTER[1] + RADIUS * math.sin(i * math.pi / 180))

		hours_init.append((x_coordinate,y_coordinate))

	for i in range(0,360,6):
		x_coordinate = int(CENTER[0] + (RADIUS-20) * math.cos(i * math.pi / 180))
		y_coordinate = int(CENTER[1] + (RADIUS-20) * math.sin(i * math.pi / 180))

		hours_dest.append((x_coordinate,y_coordinate))

	return hours_init, hours_dest

#Turn time into suitable representation
def getDigitalTime(h,m,s):
	time = ""
	hour = ""
	minute = ""
	second = ""
	if(h<10):
		hour = "0{}:".format(h)
	else:
		hour = "{}:".format(h)
	if(m<10):
		minute = "0{}:".format(m)
	else:
		minute = "{}:".format(m)
	if(s<10):
		second = "0{}".format(s)
	else:
		second = "{}".format(s)
	time = hour+minute+second
	return time

#Function for drawing the hands of teh clock
def draw_time(image):

	#getting the time from time module 
	time_now = datetime.datetime.now().time()
	hour = math.fmod(time_now.hour, 12)
	minute = time_now.minute
	second = time_now.second

	second_angle = math.fmod(second * 6 + 270, 360)
	minute_angle = math.fmod(minute * 6 + 270, 360)
	hour_angle = math.fmod((hour*30) + (minute/2) + 270, 360)

	second_x = int(CENTER[0] + (RADIUS-25) * math.cos(second_angle * math.pi / 180))
	second_y = int(CENTER[1] + (RADIUS-25) * math.sin(second_angle * math.pi / 180))
	cv2.line(image, CENTER, (second_x, second_y), COLORS['black'], 2)

	minute_x = int(CENTER[0] + (RADIUS-60) * math.cos(minute_angle * math.pi / 180))
	minute_y = int(CENTER[1] + (RADIUS-60) * math.sin(minute_angle * math.pi / 180))
	cv2.line(image, CENTER, (minute_x, minute_y), COLORS['amber'], 3)

	hour_x = int(CENTER[0] + (RADIUS-100) * math.cos(hour_angle * math.pi / 180))
	hour_y = int(CENTER[1] + (RADIUS-100) * math.sin(hour_angle * math.pi / 180))
	cv2.line(image, CENTER, (hour_x, hour_y), COLORS['amber'], 7)

	cv2.circle(image, CENTER, 5, COLORS['dark_gray'], -1)

	time = getDigitalTime(int(hour),minute,second)

	cv2.putText(image,time, (200,390), cv2.FONT_HERSHEY_DUPLEX, 1.6, COLORS['red'], 1, cv2.LINE_AA)

	return image



import cv2
import numpy as np

#Import the required attributes and helper functions
from constants import COLORS, CANVAS_SIZE, RADIUS
#import get_ticks, draw_time

#Make a empty canvas
image = np.zeros(CANVAS_SIZE, dtype=np.uint8)
#Turn it to white color
image[:] = [0,0,0]

#get the starting and ending points of ticks in the watch
hours_init, hours_dest = get_ticks()


#Draw all the ticks using for loop
for i in range(len(hours_init)):
	if i % 5 == 0:
		cv2.line(image, hours_init[i], hours_dest[i], COLORS['black'], 3)
	else:
		cv2.circle(image, hours_init[i], 5, COLORS['yellow'], -1)

#Draw some decorations on the watch
cv2.circle(image, (320,320), RADIUS+10, COLORS['red'], 2)
cv2.putText(image, "date :2022-07-28", (0,25), cv2.FONT_HERSHEY_TRIPLEX, 1, COLORS['blue'], 1)
cv2.putText(image, "time: 12:20:31" , (0,50), cv2.FONT_HERSHEY_TRIPLEX, 1, COLORS['blue'], 1)
cv2.putText(image, "clock", (215,230), cv2.FONT_HERSHEY_TRIPLEX, 2, COLORS['dark_gray'], 1, cv2.LINE_AA)

#Run until user stops
while True:
	image_original = image.copy()

	#Use draw time to make clock hands on the canvas
	clock_face = draw_time(image_original)

	#Show the watch
	cv2.imshow('clock', image_original)
	if cv2.waitKey(1)==ord('q'):
		break

cv2.destroyAllWindows()
