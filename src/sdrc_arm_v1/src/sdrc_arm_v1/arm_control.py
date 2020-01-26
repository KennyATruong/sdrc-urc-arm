#!/usr/bin/python
import rospy
import serial
import struct
import numpy as np
import time
from sensor_msgs.msg import Joy
vel_multi = 1

class arm:
    def __init__(self):
        self.velocities = {
            'wrist_roll': 0,
            'wrist_pitch': 0,
            'elbo_pitch': 0,
            'shou_pitch': 0,
            'shou_yaw': 0
        }
     
        baudrate = rospy.get_param('~baudrate', 9600)
        self.serialDev = serial.Serial(baudrate=baudrate)
        self.serialDev.port = rospy.get_param("~serial_device")
        self.serialDev.open()
        self.arm_sub = rospy.Subscriber("/joy_arm", Joy, self.arm_joy_callback)

    def write_serial(self):
      # Execute arm position
        rospy.loginfo('velocities:%s\n' % self.velocities)
        encoded_position = struct.pack("<fffff",
                                        self.velocities['wrist_roll'],
                                        self.velocities['wrist_pitch'],
                                        self.velocities['elbo_pitch'],
                                        self.velocities['shou_pitch'],
                                        self.velocities['shou_yaw'],
                                        )
        self.serialDev.write(encoded_position)

    def arm_joy_callback(self, data):
        self.velocities['wrist_roll'] = 0
        self.velocities['wrist_pitch'] = 0
        self.velocities['elbo_pitch'] = 0
        self.velocities['shou_pitch'] = 0
        self.velocities['shou_yaw'] = 0
        global vel_multi

        #slow slew mode
        if data.buttons[5] and vel_multi == 1:
            vel_multi = 0.5

        elif data.buttons[5] and vel_multi == 0.5:
            vel_multi = 1

        rospy.loginfo('vel_multi: %s', vel_multi)

        # R thumbstick left/right
        self.velocities['shou_yaw'] = data.axes[3] * -300 * vel_multi

        # R thumbstick up/down
        self.velocities['shou_pitch'] = data.axes[4] * -300 * vel_multi

        # L thumbstick up/down
        self.velocities['elbo_pitch'] = data.axes[1] * -300 * vel_multi

        # button 6 = wrist down
        # button 4 = wrist up
        if data.buttons[4]:
            self.velocities['wrist_pitch'] = 0.15 
        if data.buttons[2]:
            self.velocities['wrist_pitch'] = -0.15 

        # MOVE ARM
        self.write_serial()

def main():
    rospy.init_node("sdrc_arm_v1")
    controller = arm()
    rospy.spin()
