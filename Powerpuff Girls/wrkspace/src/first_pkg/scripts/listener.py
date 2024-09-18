#!/usr/bin/env python

#imports
import rospy
from std_msgs.msg import String

#callback 
def call(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard: %s",data.data)


#main function
    #make subscriber
    #make node
    #spin
def listen():
    rospy.Subscriber("topic",String,call)
    rospy.init_node("listener",anonymous=True)
    rospy.spin()


#function call 
if __name__=='__main__':
    listen()