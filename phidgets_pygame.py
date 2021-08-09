# Add Phidgets Library
from Phidget22.Phidget import *
from Phidget22.Devices.Accelerometer import *
from Phidget22.Devices.DigitalInput import *
from sys import exit

import pgzrun

WIDTH = 700
HEIGHT = 700

car = Actor('car', center=(WIDTH / 2, HEIGHT / 2))
background_1 = Actor('road')
background_1.right = WIDTH
background_2 = Actor('road')
background_2.right = -1400

def draw():
    screen.clear()
    background_1.draw()
    background_2.draw()
    car.draw()
    
def update():
    background_1.right += 2
    background_2.right += 2
    if background_1.right == WIDTH * 4: background_1.right = -1400
    if background_2.right == WIDTH * 4: background_2.right = -1400

    car.x += 2
    car.angle = accelerometer.getAcceleration()[0] * 90
    if car.x > WIDTH or car.x < 0: exit()
    if car.y > HEIGHT or car.y < 0: exit()

# Phidgets Code Start    
def mapAcceleration(val):
    try:
        # for simple tilting, -1 to 1 is an appropriate range
        minA = -1 
        maxA = 1
        output = ((val - minA)/(maxA - minA) * WIDTH)
        return output
    except:
        print("error")
        # if sensor is out of range, return last position
        return car.pos[1] 

def accelerate(self, state):
    car.x -= 20 - abs(car.angle / 5)
    car.y += car.angle / 5

def brake(self, state):
    car.x += 20 - abs(car.angle / 5)
    car.y -= car.angle / 5

# Create, Address, Subscribe to Events and Open
accelerometer = Accelerometer()
accelerometer.openWaitForAttachment(1000)
# accelerometer.setDataInterval(accelerometer.getMinDataInterval())

redButton = DigitalInput()
redButton.setIsHubPortDevice(True)
redButton.setHubPort(5)
redButton.setOnStateChangeHandler(brake)
redButton.openWaitForAttachment(1000)

greenButton = DigitalInput()
greenButton.setIsHubPortDevice(True)
greenButton.setHubPort(4)
greenButton.setOnStateChangeHandler(accelerate)
greenButton.openWaitForAttachment(1000)
# Phidgets Code End

pgzrun.go()
