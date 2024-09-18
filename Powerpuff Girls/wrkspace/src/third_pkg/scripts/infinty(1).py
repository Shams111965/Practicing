#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry
import math
i = -100
j = -100
desired_angle = 0
count=1
s_i=0
s_j=0
pop1=0
pop2=0
count=1
new_j=0
count1=0


def call(msg):
    global j, i, desired_angle,count,s_i,s_j
    i = msg.pose.pose.position.x
    j = msg.pose.pose.position.y
    if count:
        s_i=i
        s_j=j
        count=0
       

    rospy.loginfo(f"Current position: x={i}, y={j}")
    print(s_i)
    print(i)
    

def walk():
    global j, i, desired_angle,count,s_i,s_j,pop1,pop2,new_j,count1

    # Initialize publishers
    pub_vel = rospy.Publisher("cmd_vel", Float64, queue_size=10)
    pub_brakes = rospy.Publisher("brakes", Float64, queue_size=10)
    pub_steer = rospy.Publisher("SteeringAngle", Float64, queue_size=10)

    # Initialize the node
    rospy.init_node("walker", anonymous=True)

    # Subscribe to the odometry topic
    rospy.Subscriber('odom', Odometry, call)

    # Set rate
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
         if (abs(s_i)-i)>=0 and abs((s_i)-i)<=0.5  and pop1==5 :
                pop2=0
                pop1=0
                pub_brakes.publish(1)
                pub_vel.publish(0) 
         else :  
                if (((s_i)-i)<=12 and ((s_j)-j)<=4 ):
                    pub_steer.publish(20.7)
                    pub_vel.publish(0.2)
                    rospy.loginfo("poppp")
                if(((s_j)-j)>=4 and pop1<3 ):
                            pop1 =1 
                            rospy.loginfo("poppp")
                            print(i)
                            pop1=2
                            pub_steer.publish(0)
                            pub_vel.publish(0.1)

                if(((i)-s_i)>=2.5 and ((s_i)-i)<=3 and pop1==2 )  :
                            if count1==0:
                                new_j=j
                                count1=1
                            rospy.loginfo("hahhhhhh")
                            pub_steer.publish(-16.15)
                            pub_vel.publish(0.2)
                            pop2=1
                            pop1=3   

                if(abs((j)-new_j) >=0 and abs((j)-new_j) <=0.5 and pop2==1 and pop1==3 and abs((s_i)-i)>=9):
                            pub_steer.publish(0)
                            pub_vel.publish(0.1)
                            pop1=5                  

           
            
                       
                    

    """if(((i)-s_i)>=1 and ((s_i)-i)<=2.5 and pop1==2 )  :
                    if count1==0:
                          new_j=j
                          count1=1
                    rospy.loginfo("hahhhhhh")
                    pub_steer.publish(-16.15)
                    pub_vel.publish(0.2)
                    pop2=1
                    pop1=3
        if(abs((j)-new_j) >=0 and abs((j)-new_j) <=0.5 and pop2==1 and pop1==3 and abs((s_i)-i)>=9):
                    pub_steer.publish(0)
                    pub_vel.publish(0.2)
                    pop1=5
        if(abs(j-s_j)<=3 and pop1==5):
                          pub_steer.publish(20.7)
                          pop1=6
                    

        if (abs(s_i)-i)>=0 and abs((s_i)-i)<=0.05  and pop1==6 :
                pop2=0
                pop1=0
                pub_brakes.publish(1)
                pub_vel.publish(0)        """   



             
    rate.sleep()




if __name__ == '__main__':
    try:
        walk()
    except rospy.ROSInterruptException:
        pass
