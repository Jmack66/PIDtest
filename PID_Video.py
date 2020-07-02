import numpy as np
import matplotlib.pyplot as plt
import turtle 
import time

#GLOBAL PARAMS
TIMER = 0
TIME_STEP = 0.001
SETPOINT = 400
SIM_TIME = 500
INITIAL_X = 0
INITIAL_Y = -100
MASS = 1 #kg
MAX_THRUST = 15 #Newtons
g = -9.81 #Gravitational constant
V_i = 0 #initial velocity 
Y_i = 0 #initial height
#------------
#---PID GAINS--- 
#ku = 0.6
#Tu = 18 ms
KP = 0.36
KI = 40.0
KD = 0.0008099999999999997
# KP = 0.6
# KI = 0.0
# KD = 0.0
#---------------

class Simulation(object):
	def __init__(self):
		self.Insight = Rocket()
		self.pid = PID(KP,KI,KD,SETPOINT)
		self.screen = turtle.Screen()
		self.screen.setup(1280,900)
		self.marker = turtle.Turtle()
		self.marker.penup()
		self.marker.left(180)
		self.marker.goto(15,SETPOINT)
		self.marker.color('red')
		self.sim = True
		self.timer = 0
		self.poses = np.array([])
		self.times = np.array([])
	def cycle(self):
		while(self.sim):
			thrust = self.pid.compute(self.Insight.get_y())
			print(thrust)
			self.Insight.set_ddy(thrust)
			self.Insight.set_dy()
			self.Insight.set_y()
			time.sleep(TIME_STEP)
			self.timer += 1
			if self.timer > SIM_TIME:
				print("SIM ENDED")
				self.sim = False
			elif self.Insight.get_y() > 800:
				print("OUT OF BOUNDS")
				self.sim = False
			elif self.Insight.get_y() < -800:
				print("OUT OF BOUNDS")
				self.sim = False
			self.poses = np.append(self.poses,self.Insight.get_y())
			self.times = np.append(self.times,self.timer)
		graph(self.times,self.poses)

def graph(x,y):
	plt.plot(x,y)
	plt.show()


class Rocket(object):
	def __init__(self):
		global Rocket
		self.Rocket = turtle.Turtle()
		self.Rocket.shape('square')
		self.Rocket.color('black')
		self.Rocket.penup()
		self.Rocket.goto(INITIAL_X,INITIAL_Y)
		self.Rocket.speed(0)
		#physics
		self.ddy = 0
		self.dy = V_i
		self.y = INITIAL_Y
	def set_ddy(self,thrust):
		self.ddy = g + thrust / MASS
	def get_ddy(self):
		return self.ddy
	def set_dy(self):
		self.dy += self.ddy
	def get_dy(self):
		return self.dy
	def set_y(self):
		self.Rocket.sety(self.y + self.dy)
	def get_y(self):
		self.y = self.Rocket.ycor()
		return self.y

class PID(object):
	def __init__(self,KP,KI,KD,target):
		self.kp = KP
		self.ki = KI
		self.kd = KD 
		self.setpoint = target
		self.error = 0
		self.integral_error = 0
		self.error_last = 0
		self.derivative_error = 0
		self.output = 0
	def compute(self, pos):
		self.error = self.setpoint - pos
		self.integral_error += self.error * TIME_STEP
		self.derivative_error = (self.error - self.error_last) / TIME_STEP
		self.error_last = self.error
		self.output = self.kp*self.error + self.ki*self.integral_error + self.kd*self.derivative_error
		if self.output >= MAX_THRUST:
			self.output = MAX_THRUST
		elif self.output <= 0:
			self.output = 0
		return self.output

def main():
	sim = Simulation()
	sim.cycle()

main()
