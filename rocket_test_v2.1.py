import turtle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

def main():
	MASS = 1 #kg
	MAX_THRUST = 15 #Newtons
	g = -9.81 #Gravitational constant
	V_i = 0 #initial velocity 
	Y_i = 0 #initial height
	#--------PID GAINS--------
	kp = 0.2 
	ki = 0.032	
	kd = 0.1	
	SETPOINT = 10
	initScreen()
	initMarker(SETPOINT)
	initRocket()


def initMarker(SETPOINT):
	marker = turtle.Turtle()
	marker.penup()
	marker.left(180)
	marker.goto(15, SETPOINT)
	marker.color("red")
def initRocket():
	rocket = turtle.Turtle()
	rocket.shape('square')
	rocket.penup()
	rocket.speed(0)
	rocket.goto(0,-100)
def initScreen():
	global screen
	screen = turtle.Screen()
	screen.setup(800,800)

def get_ddy(thrust):
	return (g + thrust/MASS)

def get_dy(ddy):
	dy += ddy
	return dy

class Rocket:
	def __init__(self):
		self.ddy = g
		self.dy = V_i
		self.y = Y_i
		self.thrust = thrust
	def get_ddy(self,thrust):
		self.ddy = g + self.thrust/MASS
		return self.ddy
	def get_dy(self):
		self.dy += self.ddy
		return  self.dy
	def get_y(self):
		self.y = rocket.ycor()
		return self.y
main()