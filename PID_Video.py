import numpy as np
import matplotlib.pyplot as plt
import turtle 
import time

#GLOBAL PARAMS
TIMER = 0
TIME_STEP = 0.001
SETPOINT = 10
SIM_TIME = 100
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
#KD = 0.00128 for higher setpoints
antiWindup = True
# KP = 0.6
# KI = 0.0
# KD = 0.0
#---------------

class Simulation(object):
	def __init__(self):
		self.Insight = Rocket()
		self.pid = PID(KP,KI,KD,SETPOINT)
		self.screen = turtle.Screen()
		self.screen.setup(800,600)
		self.marker = turtle.Turtle()
		self.marker.penup()
		self.marker.left(180)
		self.marker.goto(15,SETPOINT)
		self.marker.color('red')
		self.sim = True
		self.timer = 0
		self.poses = np.array([])
		self.times = np.array([])
		self.kpe = np.array([])
		self.kde = np.array([])
		self.kie = np.array([])
		self.thrst = np.array([])
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
			elif self.Insight.get_y() > 700:
				print("OUT OF BOUNDS")
				self.sim = False
			elif self.Insight.get_y() < -700:
				print("OUT OF BOUNDS")
				self.sim = False
			self.poses = np.append(self.poses,self.Insight.get_y())
			self.times = np.append(self.times,self.timer)
			self.kpe = np.append(self.kpe,self.pid.get_kpe())
			self.kde = np.append(self.kde,self.pid.get_kde())
			self.kie = np.append(self.kie,self.pid.get_kie())
			self.thrst = np.append(self.thrst,thrust)
		graph(self.times,self.poses,self.kpe,self.kde,self.kie,self.thrst)

def graph(x,y1,y2,y3,y4,y5):
	fig, (ax1, ax2,ax3,ax4,ax5) = plt.subplots(5, sharex=True)
	#fig.suptitle('antiwindup')
	ax1.set(ylabel='rocket \nHeight')
	ax1.plot(x,y1)
	ax2.set(ylabel='KP_error')
	ax2.plot(x,y2,'tab:red')
	ax3.set(ylabel='KD_error')
	ax3.plot(x,y3,'tab:orange')
	ax4.set(ylabel='KI_error')
	ax4.plot(x,y4,'tab:pink')
	ax5.set(ylabel='rocket \nThrust')
	ax5.plot(x,y5,'tab:brown')
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
		self.dy += self.ddy * TIME_STEP
	def get_dy(self):
		return self.dy
	def set_y(self):
		self.Rocket.sety(self.y + self.dy * TIME_STEP)
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
		#self.integral_error += self.error * TIME_STEP
		self.derivative_error = (self.error - self.error_last) / TIME_STEP
		self.error_last = self.error
		self.output = self.kp*self.error + self.ki*self.integral_error + self.kd*self.derivative_error
		if(abs(self.output)>= MAX_THRUST and (((self.error>=0) and (self.integral_error>=0))or((self.error<0) and (self.integral_error<0)))):
			if(antiWindup):
				#no integration
				self.integral_error = self.integral_error
			else:
				#if no antiWindup rectangular integration
				self.integral_error += self.error * TIME_STEP
		else:
			#rectangular integration
			self.integral_error += self.error * TIME_STEP
		if self.output >= MAX_THRUST:
			self.output = MAX_THRUST
		elif self.output <= 0:
			self.output = 0
		return self.output
		
	def get_kpe(self):
		return self.kp*self.error
	def get_kde(self):
		return self.kd*self.derivative_error
	def get_kie(self):
		return self.ki*self.integral_error

def main():
	sim = Simulation()
	sim.cycle()

main()
