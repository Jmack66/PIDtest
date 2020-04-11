import turtle
import numpy as np
import matplotlib

screen = turtle.Screen()
screen.setup(1000,800)

rocket = turtle.Turtle()
rocket.shape('square')
ypos = 0
rocket.left(90)
rocket.penup()
while ypos < 300:
	ypos = ypos + 1
	rocket.forward(ypos)

	



