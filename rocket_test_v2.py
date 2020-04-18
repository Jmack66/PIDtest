import turtle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import sys
#--------------------------
#sytle.use('fivethirtyeight')
# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)
# lines = plt.plot([])
# line = lines[0]
mass = 1 #kg
max_thrust = 15
g = -9.81 #ms^-2
v_i = 0 #start at 0 m/s
h_i = 0 #start at 0 m
kp = 0.55 	#pid gains----
ki = 0	#pid gains----
kd = 0.8	#pid gains----
setpoint = 10
errorsum = 0
last_error = 0
rocket = turtle.Turtle()
rocket.shape('square')
rocket.penup()
rocket.speed(0)
rocket.goto(0,-100)
marker = turtle.Turtle()
marker.penup()
marker.left(180)
marker.goto(15,setpoint)
marker.color("red")


def initScreen():
	global screen
	screen = turtle.Screen()
	screen.setup(800,800)
	#screen.tracer(0)

def ddy(thrust):
	if thrust > max_thrust:
		thrust = max_thrust
	elif thrust < 0:
		thrust = 0
	return (g + thrust/mass)

def computePID2(height):
	global errorsum,last_error
	error = setpoint-height
	errorsum += error
	error_d = error - last_error
	output = kp*error + ki*errorsum + kd*error_d
	return output

#add functionality to plot points
def main():
	initScreen()
	sim = True
	dy = 0
	thrust = 0
	y = 0
	t = 0
	while sim is True:
		#screen.update()
		thrust = computePID2(y)
		print(thrust)
		dy += ddy(thrust)
		y = rocket.ycor()
		rocket.sety(y + dy)
		time.sleep(0.05)
		if y > 800:
			sim = False
		elif y < -800:
			sim = False

main()
# Set all gains to zero.
# Increase the P gain until the response to a disturbance is steady oscillation.
# Increase the D gain until the the oscillations go away (i.e. it's critically damped).
# Repeat steps 2 and 3 until increasing the D gain does not stop the oscillations.
# Set P and D to the last stable values.
# Increase the I gain until it brings you to the setpoint with the number of oscillations desired (normally zero but a quicker response can be had if you don't mind a couple oscillations of overshoot)
