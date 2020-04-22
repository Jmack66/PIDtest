import turtle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib import style
global timestep,MASS,MAX_THRUST,g,V_i,Y_i,kp,ki,kdSETPOINT
timestep = 0.05
MASS = 1 #kg
MAX_THRUST = 15 #Newtons
g = -9.81 #Gravitational constant
V_i = 0 #initial velocity 
Y_i = 0 #initial height
#--------PID GAINS--------
kp = 0.00 
ki = 0.00	
kd = 0.00	
SETPOINT = 10
def main():
	sim = True
	r = Rocket()
	pid = PID(kp,ki,kd,SETPOINT)
	ddy = 0
	dy = 0
	y = 0
	while sim:
		thrust = pid.compute(y)
		ddy = r.get_ddy(thrust)
		dy = r.get_dy()
		y = rocket.ycor()
		y = r.get_y(y)
		rocket.sety(y + dy)
		time.sleep(timestep)
		if y > 800:
			sim = False
		elif y < -800:
			sim = False


def initMarker(SETPOINT):
	global marker
	marker = turtle.Turtle()
	marker.penup()
	marker.left(180)
	marker.goto(15, SETPOINT)
	marker.color("red")
def initRocket():
	global rocket
	rocket = turtle.Turtle()
	rocket.shape('square')
	rocket.penup()
	rocket.speed(0)
	rocket.goto(0,-100)
def initScreen():
	global screen
	screen = turtle.Screen()
	screen.setup(800,800)
	
class Rocket:
	def __init__(self):
		self.ddy = 0
		self.dy = V_i
		self.y = Y_i
	def get_ddy(self,thrust):
		self.ddy = g + thrust / MASS
		return self.ddy
	def get_dy(self):
		self.dy += self.ddy
		return  self.dy
	def get_y(self,y):
		self.y = y
		return self.y

class PID:
	def __init__(self,kp,ki,kd,SETPOINT):
		self.kp = kp
		self.ki = ki
		self.kd = kd
		self.errorsum = 0
		self.last_error = 0
		self.error = 0
		self.error_d = 0
		self.setpoint = SETPOINT
		self.output = 0
	def compute(self, height):
		self.error = self.setpoint - height
		self.errorsum += self.error * timestep
		self.error_d = (self.error - self.last_error)/timestep
		self.output = self.kp*self.error + self.ki*self.errorsum + self.kd*self.error_d
		if self.output > MAX_THRUST:
			self.output = 15
		elif self.output < 0:
			self.output = 0
		self.last_error = self.error
		return self.output
initScreen()
initMarker(SETPOINT)
initRocket()
main() 