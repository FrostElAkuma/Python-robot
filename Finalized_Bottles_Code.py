
import time
import random
import sys
sys.path.append('../')

from Common_Libraries.p3b_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim():
    try:
        my_table.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

### Constants
speed = 0.2 #Qbot's speed

### Initialize the QuanserSim Environment
my_table = servo_table()
arm = qarm()
arm.home()
bot = qbot(speed)

#######################################################################


import random

bottle = [1,2,3]
bottle_properties = []
bottle_qbot = []


def dispense_container(bottle): 
    properties = my_table.container_properties(bottle)
    my_table.dispense_container()
    return properties



def arm_movement():
    arm.rotate_elbow(-23)
    arm.rotate_shoulder(50)
    arm.rotate_elbow(-15)
    arm.control_gripper(45) 
    arm.rotate_elbow(-3)
    arm.move_arm(0, -0.2, 0.5)
    arm.rotate_elbow(-20)
    #arm.rotate_shoulder(35)

import random

bottle = [1,2,3]
bottle_properties = []
bottle_qbot = []


def dispense_container(bottle): 
    properties = my_table.container_properties(bottle)
    my_table.dispense_container()
    return properties



def arm_movement():
    arm.rotate_elbow(-23)
    arm.rotate_shoulder(50)
    arm.rotate_elbow(-15)
    arm.control_gripper(45) 
    arm.rotate_elbow(-3)
    arm.move_arm(0, -0.2, 0.5)
    arm.rotate_elbow(-20)
    #arm.rotate_shoulder(35)

def loading_container1():
    global bottle_properties #global updates and let us use the variable that is not defined inside the function
    global bottle_qbot
    weight = 0
    total_bottles = 0
    base = 30

    for i in range (4):
        bottle_properties.append(dispense_container(random.choice(bottle)))
        total_bottles += 1
        weight =+ bottle_properties[i][1]
        if weight < 90 and total_bottles <= 3 and bottle_properties[i][2] == bottle_properties[0][2]:
            arm_movement()
            arm.rotate_base(base - 13)
            base = base - 13
            arm.rotate_shoulder(35)
            arm.control_gripper(-45)
            arm.rotate_shoulder(-50)
            arm.home()
        else:
            bottle_qbot = bottle_properties[0] #The first bottle to be placed on the qbot 
            last_bottle = bottle_properties[i]
            bottle_properties = []
            bottle_properties.append(last_bottle)
            break

def loading_container2():
    global bottle_qbot
    global bottle_properties
    weight = bottle_properties[0][1]
    total_bottles = 0
    base = 30

    if weight < 90:
        total_bottles += 1
        arm_movement()
        arm.rotate_base(base - 13)
        base = base - 13
        arm.rotate_shoulder(35)
        arm.control_gripper(-45)
        arm.rotate_shoulder(-50)
        arm.home()


    for i in range (4):
        i += 1 #Because there is a bottle placed thus start counting from the second bottle
        bottle_properties.append(dispense_container(random.choice(bottle)))
        total_bottles += 1
        weight += bottle_properties[i][1]
        if weight < 90 and total_bottles <= 3 and bottle_properties[i][2] == bottle_properties[0][2]:
            arm_movement()
            arm.rotate_base(base - 13)
            base =base - 13
            arm.rotate_shoulder(35)
            arm.control_gripper(-45)
            arm.rotate_shoulder(-50)
            arm.home()
        else:
            bottle_qbot = bottle_properties[0]
            last_bottle = bottle_properties[i]
            bottle_properties = []
            bottle_properties.append(last_bottle)
            break

    

    
def qbot_sensor():
    #global bottle_properties
    global bottle_qbot
    #print(bottle_qbot)
    if bottle_qbot[2] == 'Bin01':
        bot.activate_color_sensor("Red")
        for i in range (99):
            bot.forward_speed(0.2)
            voltage = bot.read_red_color_sensor("Bin01",1)
            average = (voltage[0] + voltage[1] + voltage[2] + voltage[3] + voltage[4]) / 5
            if average >= 4 and average <=5:
                break

    if bottle_qbot[2] == 'Bin02':
         bot.activate_color_sensor("Blue")
         for i in range (99):
             bot.forward_speed(0.2)
             voltage = bot.read_blue_color_sensor("Bin02",1)
             average = (voltage[0] + voltage[1] + voltage[2] + voltage[3] + voltage[4]) / 5
             if average >= 4 and average <=5:
                 break
                
    if bottle_qbot[2] == 'Bin03':
        bot.activate_color_sensor("Green")
        for i in range (99):
            bot.forward_speed(0.2)
            voltage = bot.read_green_color_sensor("Bin03",1)
            average = (voltage[0] + voltage[1] + voltage[2] + voltage[3] + voltage[4]) / 5
            if average >= 4 and average <=5:
                break   



def qbot_movement():
    bot.forward_time(3.6)
    bot.activate_actuator()
    bot.dump()
    bot.deactivate_actuator()
    lost_line = 0   
    while lost_line<2:
        lost_line, velocity = bot.follow_line(0.3)
        bot.forward_velocity(velocity)
    bot.rotate(191)



on = True

loading_container1()
while on == True:
    qbot_sensor()
    qbot_movement()
    loading_container2()

#Anas/Abdullah 2021-02-24
