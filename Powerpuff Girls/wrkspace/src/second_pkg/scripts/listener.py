#!/usr/bin/env python

#imports
import rospy
from geometry_msgs.msg import Pose2D
import matplotlib.pyplot as plt
import numpy as np
import time

#callback function
def call(msg):
    rospy.loginfo(f"I heard {msg.theta*(180/np.pi)}")
    plt.plot(msg.x,msg.y,marker=(3,0,msg.theta*(180/np.pi)*90), markersize=20, linestyle='None', color='green')
    plt.axis('equal')
    plt.draw()
    plt.pause(0.01)


#main function
def listen():
    #make a subscriber
    rospy.Subscriber('pioneer/pose',Pose2D,call) #topic should match that in coppeliaSim
    #make a node
    rospy.init_node('sub',anonymous=True)
    #spin
    rospy.spin()

#call main function
if __name__=='__main__':
        listen()
