#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import blynklib
import time

BLYNK_AUTH = '1NQy64vJg3TS9QeC9scpf7LXzzYcB-q-'

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"

JoyX = 0
JoyY = 0

# register handler for virtual pin V4 write event
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin,value):
    #print(int(value[0]))
    global JoyX,JoyY
    JoyX = int(value[0])
    JoyY = int(value[1])

###########################################################
# infinite loop that waits for event
###########################################################
if __name__ == "__main__":
    rospy.init_node('blynk_Vel')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    while True:
        blynk.run()
        time.sleep(0.1)
        #print('JoyX  {} , JoyY  {} '.format(JoyX,JoyY))
        blynk_twist = Twist()

        if abs(JoyY) < 60:
            blynk_twist.linear.x = 0
        else:
            blynk_twist.linear.x = float(JoyY)/1000

        blynk_twist.linear.y = 0.0
        blynk_twist.linear.z = 0.0
        blynk_twist.angular.x = 0.0
        blynk_twist.angular.y = 0.0

        if abs(JoyX) < 60:
            blynk_twist.angular.z = 0
        else:
            blynk_twist.angular.z = float(JoyX * (-1))/1000
       
        
        pub.publish(blynk_twist)