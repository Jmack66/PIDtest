import turtle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib import style
timestep = 0.05 #sets how quickly the simulation refreshes (0.05 is a happy medium)
MASS = 1 #kg
MAX_THRUST = 15 #Newtons
g = -9.81 #Gravitational constant
V_i = 0 #initial velocity 
Y_i = 0 #initial height
#--------PID GAINS--------
kp = 0.2
ki = 0.0
kd = 0.0
#-------------------------
SETPOINT = 10

def main():
	sim1 = Simulation()
	sim1.cycle()

class Simulation:
	def __init__(self):
		self.screen = turtle.Screen()
		self.screen.setup(1200,800)
		self.marker = turtle.Turtle()
		self.marker.penup()
		self.marker.left(180)
		self.marker.goto(15,SETPOINT)
		self.marker.color('red')
		self.sim = True
		self.timer = 0
		self.pos = np.array([])
		self.velocity = np.array([])
		self.times = np.array([])
		self.period = np.array([])

	def cycle(self):
		r = Rocket()
		pid = PID(kp,ki,kd,SETPOINT)
		positive = True
		while self.sim:
			thrust = pid.compute(r.get_y())
			r.set_ddy(thrust)
			r.set_dy()
			r.set_y()
			time.sleep(timestep)
			self.timer += timestep
			if r.get_y() > 800:
			 	self.sim = False
			 	print("OUT OF BOUNDS")
			elif r.get_y() < -800:
				print("OUT OF BOUNDS")
				self.sim = False
			if self.timer > 10:
				print("SIM TIME END")
				self.sim = False
			self.times = np.append(self.times, self.timer)
			self.velocity = np.append(self.velocity, r.get_dy())
			self.pos = np.append(self.pos, r.get_y())
			if r.get_dy() < 0:
				if positive == True:
					positive = False
					self.period = np.append(self.period, self.timer)
			if r.get_dy() > 0:
				if positive == False:
					positive = True
					self.period = np.append(self.period, self.timer)
		period = np.mean(self.period) / 2
		print(period)
		graph(self.times, self.pos)

def graph(x,y):
	plt.plot(x,y)
	plt.show()

class Rocket:
	def __init__(self):
		global rocket
		rocket = turtle.Turtle()
		rocket.shape('square')
		rocket.penup()
		rocket.speed(0)
		rocket.goto(0,-100)
		self.ddy = 0
		self.dy = V_i
		self.y = Y_i
	def set_ddy(self,thrust):
		self.ddy = g + thrust / MASS
	def get_ddy(self):
		return self.ddy
	def set_dy(self):
		self.dy += self.ddy
	def get_dy(self):
		return self.dy
	def set_y(self):
		rocket.sety(self.y + self.dy)
	def get_y(self):
		self.y = rocket.ycor()
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

main() 
