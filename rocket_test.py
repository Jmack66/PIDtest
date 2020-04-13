import turtle
import numpy as np
import matplotlib
last_error = 0
errorsum = 0
mass = 1 #kg
g = -9.81 #ms^-2
v_i = 0 #start at 0 m/s
h_i = 0 #start at 0 m
kp = 0 	#pid gains----
ki = 0	#pid gains----
kd = 1	#pid gains----
time_step = 0.01
setpoint = 10
rocket = turtle.Turtle()
rocket.shape('square')
rocket.penup()
rocket.goto(0,-1)
marker = turtle.Turtle()
marker.penup()
marker.left(180)
marker.goto(15,setpoint)
marker.color("red")

def initScreen():
	screen = turtle.Screen()
	screen.setup(800,800)
def rocketAccel(thrust):
	return g*mass + thrust/mass
def rocketVel(accel,time):
	return (accel*time + v_i)*(1/time_step)
def rocketAlt(velocity, time):
	return (velocity*time + h_i)*(1/time_step)
def computePID2(height):
	global errorsum
	error = setpoint-height
	errorsum = errorsum + (error*time_step)
	error_d = (error - last_error)/time_step
	output = kp*error + ki*errorsum + kd*error_d
	print(output)
	if output > 20:
		output = 20
	if output < 0:
		output = 0
	last_error == error
	return output
def main():
	initScreen()
	time = 0.00
	sim = True
	thrust = 0
	while sim is True:
		h_dd = rocketAccel(thrust)
		h_d = rocketVel(h_dd, time)
		h = rocketAlt(h_d, time)
		thrust = computePID2(h)
		#print(thrust,h)
		#print(setpoint)
		rocket.goto(0,h)
		time = time + time_step
		if h > 800:
			sim = False
		elif h < -800:
			sim = False

main()

# Set all gains to zero.
# Increase the P gain until the response to a disturbance is steady oscillation.
# Increase the D gain until the the oscillations go away (i.e. it's critically damped).
# Repeat steps 2 and 3 until increasing the D gain does not stop the oscillations.
# Set P and D to the last stable values.
# Increase the I gain until it brings you to the setpoint with the number of oscillations desired (normally zero but a quicker response can be had if you don't mind a couple oscillations of overshoot)
