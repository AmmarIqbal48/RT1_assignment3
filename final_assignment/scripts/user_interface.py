#!/usr/bin/env python3
import rospy
import actionlib
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# Initialize some global variables
mode = ''    # store the command insert by the user
pub= None       # publisher to /cmd_vel




#########################################################################################################################

'''
    Function that is used to get a goal position inside the map to be sent to
    the /move_base node.
      Args:
        - void
      Return:
        - target: an array of two integers that contains the (x, y) coordinates
                  of the point to reach;
'''
def get_goal():
    # initialize the target coordinates
    x= ''
    y= ''

    # ask for the x coordinate until the user enters an admissable value
    while x is not int:
        try:
            x= int(input('x: '))
            break
        except ValueError:
            print('Please enter a valid number.')

    # ask for the y coordinate until the user enters an admissable value
    while y is not int:
        try:
            y= int(input('y: '))
            break
        except ValueError:
            print('Please enter a valid number.')

    return x, y


#####################################################################################################################################

# Callback functions
'''
    Function that is called each time that a new message on the /automatic/cmd_vel
    topic is published. The function is used to published it on the /cmd_vel topic
    when the user has selected the corresponding mode.
      Args:
        - msg: Twist message that contains the velocity generated by the move_base node;
      Return:
        - void
'''
def auto_drive_callback(msg):
    global mode, pub

    # If the user has selected the automatic mode, publish the message on /cmd_vel
    if (mode == '1'):
        pub.publish(msg)

'''
    Function that is called each time that a new message on the /manual/cmd_vel
    topic is published. The function is used to published it on the /cmd_vel topic
    when the user has selected the corresponding mode.
      Args:
        - msg: Twist message that contains the velocity generated by the teleop_twist_keyboard node;
      Return:
        - void
'''
def man_vel_callback(msg):
    global mode, pub

    # If the user has selected the manual mode, publish the message on /cmd_vel
    if (mode == '2'):
        pub.publish(msg)

'''
    Function that is called each time that a new message on the /assisted/cmd_vel
    topic is published. The function is used to published it on the /cmd_vel topic
    when the user has selected the corresponding mode.
      Args:
        - msg: Twist message that contains the velocity generated by the collision_avoidance node;
      Return:
        - void
'''
def astd_vel_callback(msg):
    global mode, pub

    # If the user has selected the assisted mode, publish the message on /cmd_vel
    if (mode == '3'):
        pub.publish(msg)








def main():
    # initialize the node
    rospy.init_node('user_interface')

    global mode, pub

    # define a subscriber to the /automatic/cmd_vel topic, which is the one on
    # which the move_base node publishes
    sub1= rospy.Subscriber('/automatic/cmd_vel', Twist, auto_drive_callback)

    # define a subscriber to the /manual/cmd_vel topic, which is the one on
    # which the teleop_twist_keyboard node publishes
    sub2= rospy.Subscriber('/manual/cmd_vel', Twist, man_vel_callback)

    # define a subscriber to the /assisted/cmd_vel topic, which is the one on
    # which the teleop_twist_keyboard node publishes
    sub3= rospy.Subscriber('/assisted/cmd_vel', Twist, astd_vel_callback)

    # define a publisher on the /cmd_vel topic, which is the one read by the simulation
    # environment to move the robot inside the map 
    pub= rospy.Publisher('/cmd_vel', Twist, queue_size= 1)

    # define an action client called 'move_base'
    client= actionlib.SimpleActionClient('move_base', MoveBaseAction)
    # wait until the action server has started up and started listening for goals
    client.wait_for_server()
    # create a new goal with the MoveBaseGoal constructor and fill the constant fields
    goal= MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.orientation.w = 1.0       # no rotation w.r.t. the map frame


    # infinite loop that allows the user to change driving mode continuosly
    while not rospy.is_shutdown():
        # display the instructions to use the ui
        
        print ("""                     ****   MENU   ****
                           ......
                            ....
                             .. 
                    
            1) --> TO DRIVE THE ROBOT AUTONOMOUSLY PRESS 1
            
            2) --> TO DRIVE THE ROBOT MANUALLY PRESS 2
            
            3) --> TO DRIVE THE ROBOT MANUALLY WITH ASSISTIVE MODE PRESS 3 """  )
            
        mode = input('Select a driving mode or press \'q\' to exit: ')

        # autonomous mode
        if (mode == '1'):
            print('\n========================================================================\n')
            print('AUTONOMOUS MODE')
            nav_cmd= ''
            while (nav_cmd != 'b'):
                print('\nInsert the goal position (x, y) to reach...')
                my_goal= get_goal();

                # update the message to be published on the /move_base/goal topic
                goal.target_pose.pose.position.x= my_goal[0]
                goal.target_pose.pose.position.y= my_goal[1]

                # send the goal to the action server
                client.send_goal(goal)

                print('\nEnter \'b\' at any time to return nav_cmd to the main menu or press \'g\' to')
                print('insert a new goal...')
                nav_cmd= ''
                while (nav_cmd != 'g') and (nav_cmd != 'b'):
                    nav_cmd= input()
                    if (nav_cmd != 'g') and (nav_cmd != 'b'):
                        print('Please, try again.')

                # cancel the current goal
                client.cancel_goal()

            # set the velocity to zero before returning to the main menu
            null_vel= Twist()
            null_vel.linear.x= 0
            null_vel.angular.z= 0
            pub.publish(null_vel)

        # manual mode
        elif (mode == '2'):
            print('\n========================================================================\n')
            print('MANUAL MODE\n')
            print('Switch to the teleop_twist_keyboard node to control the robot.')

            print('\nEnter \'b\' at any time to return nav_cmd to the main menu...')
            nav_cmd= ''
            while (nav_cmd != 'b'):
                nav_cmd= input()
                if(nav_cmd != 'b'):
                    print('Please, try again.')

            # set the velocity to zero before returning to the main menu
            null_vel= Twist()
            null_vel.linear.x= 0
            null_vel.angular.z= 0
            pub.publish(null_vel)

        # assisted mode
        elif (mode == '3'):
            print('\n========================================================================\n')
            print('ASSISTED MODE\n')
            print('Switch to the teleop_twist_keyboard node to control the robot.')

            print('\nEnter \'b\' at any time to return nav_cmd to the main menu...')
            nav_cmd= ''
            while (nav_cmd != 'b'):
                nav_cmd= input()
                if(nav_cmd != 'b'):
                    print('Please, try again.')

            # set the velocity to zero before returning to the main menu
            null_vel= Twist()
            null_vel.linear.x= 0
            null_vel.angular.z= 0
            pub.publish(null_vel)

        # exit
        elif (mode == 'q'):
            break

        # invalid command
        else:
            print('Invalid command, please try again.\n')




if __name__ == '__main__':
    main()
