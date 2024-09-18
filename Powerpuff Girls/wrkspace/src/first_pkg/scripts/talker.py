#!/usr/bin/env python


import rospy 
from std_msgs.msg import String


#main function
def talk():
    #make pubisher
    pub=rospy.Publisher("topic",String,queue_size=10)
    #make node
    rospy.init_node("talker",anonymous=True)
    #set rate
    rate=rospy.Rate(10) #in HZ
    #write & publish string
    while not rospy.is_shutdown():
        msg=f"welcome {rospy.get_time()}"
        rospy.loginfo(msg)
        pub.publish(msg)
        #sleep
        rate.sleep()


#function call with exception check
if __name__=='__main__':
    try:
        talk()
    except rospy.ROSInterruptException:
        pass 