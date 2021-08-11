# Add Phidgets Library
from Phidget22.Phidget import *
from Phidget22.Devices.Accelerometer import *
from Phidget22.Devices.DigitalInput import *
from datetime import datetime
from sys import exit

import pgzrun

# Set Game Board Dimensionsw
WIDTH = 700
HEIGHT = 700

car = Actor('car', center=(WIDTH / 2, HEIGHT / 2))
background_1 = Actor('road')
background_1.right = WIDTH
background_2 = Actor('road')
background_2.right = -1400
game_speed = 1 # Speed at which everything moves

def increase_game_speed():
    global game_speed
    game_speed += 1

clock.schedule_interval(increase_game_speed, 10)

def draw():
    screen.clear()
    background_1.draw()
    background_2.draw()
    car.draw()
    # Draw helpful text
    screen.draw.text("TIME: " + str(int(timer)), (20, 20), fontsize=40, owidth=1)
    screen.draw.text("LEVEL " + str(game_speed), topright=(680, 20), fontsize=40, owidth=1)

initial_time = datetime.now().timestamp()

def update():
    global timer
    timer = datetime.now().timestamp() - initial_time

    background_1.right += game_speed
    background_2.right += game_speed
    car.x += game_speed

    # Reset background to original position once it leaves the area
    if background_1.right >= WIDTH * 4: background_1.right = -1400
    if background_2.right >= WIDTH * 4: background_2.right = -1400

    # Turn the car
    animate(car, duration=0.1, angle=(accelerometer.getAcceleration()[0] * 90))
    # Move the car
    if accel: animate(car, duration=0.1, pos=(car.x - (20 + level * 2 - abs(car.angle / 5)), car.y + (car.angle / 4)))
    if reverse: animate(car, duration=0.1, pos=(car.x + (20 - abs(car.angle / 5)), car.y - (car.angle / 4)))
    # End the game
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

def accelerateHook(self, state):
    global accel
    if state: accel = True
    else: accel = False

def reverseHook(self, state):
    global reverse
    if state: reverse = True
    else: reverse = False

# Create, Address, Subscribe to Events and Open
accelerometer = Accelerometer()
accelerometer.openWaitForAttachment(1000)
accelerometer.setDataInterval(accelerometer.getMinDataInterval())

redButton = DigitalInput()
redButton.setIsHubPortDevice(True)
redButton.setHubPort(1)
redButton.setOnStateChangeHandler(reverseHook)
redButton.openWaitForAttachment(1000)

greenButton = DigitalInput()
greenButton.setIsHubPortDevice(True)
greenButton.setHubPort(4)
greenButton.setOnStateChangeHandler(accelerateHook)
greenButton.openWaitForAttachment(1000)
# Phidgets Code End

pgzrun.go()
