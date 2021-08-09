# Add Phidgets Library
from Phidget22.Phidget import *
from Phidget22.Devices.Accelerometer import *

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
    background_1.right += 1
    background_2.right += 1
    if background_1.right == WIDTH * 4: background_1.right = -1400
    if background_2.right == WIDTH * 4: background_2.right = -1400

    output = mapAcceleration(accelerometer.getAcceleration()[0])
    car.pos = WIDTH / 2, output

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

# Create, Address, Subscribe to Events and Open
accelerometer = Accelerometer()
accelerometer.openWaitForAttachment(1000)
# Set data interval to minimum 
accelerometer.setDataInterval(accelerometer.getMinDataInterval())
# Phidgets Code End

pgzrun.go()
