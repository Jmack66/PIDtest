import turtle
import numpy as np
import matplotlib
mass = 1 #kg
g = -9.81 #ms^-2
thrust = 10 #newtons
v_i = 0 #start at 0 m/s
h_i = 0 #start at 0 m
rocket = turtle.Turtle()
rocket.shape('square')
rocket.penup()

def initScreen():
	screen = turtle.Screen()
	screen.setup(1000,800)
def rocketAccel(thrust):
	return g*mass + thrust/mass
def rocketVel(accel,time):
	return accel*time + v_i
def rocketAlt(velocity, time):
	return velocity*time + h_i

def main():
	initScreen()
	time = 0.00
	sim = True
	while sim is True:
		h_dd = rocketAccel(thrust)
		h_d = rocketVel(h_dd, time)
		h = rocketAlt(h_d, time)
		print(h)
		rocket.goto(0,h)
		time = time + 1
		if h > 500:
			sim = False

main()


