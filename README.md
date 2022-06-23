# RT1_Assignment3 

![image](https://user-images.githubusercontent.com/104999107/175319134-b176e12a-ffb1-44e7-954a-a002ee869f38.png)

## Introduction  

This is the third Assignment of the course Research_Track_1 in this Assignment  we asked  to create architecture on ROS and its softwear capable of controlling a mobile robot in given enviroment along with  creating a multiple modes for the user in  which  user allow to choose how to control the robot.

**_FOLLOWING ARE THE MODE_**


* --> **TO DRIVE THE ROBOT AUTONOMOUSLY**: This Mode ask the user to set the position and than robot will go to that position by itself with avoiding the obsticals
            
* --> **TO DRIVE THE ROBOT MANUALLY**:In this mode  robot is completely operated by the user manually by using the keyboard. 
            
* --> **TO DRIVE THE ROBOT MANUALLY WITH ASSISTIVE MODE**: In this mode robot is operated by the user manually by using the keyboard but this also assist the user to   prevent the robot to smash into walls 
 
 **USER_INTERFACE**
![image](https://user-images.githubusercontent.com/104999107/174690203-eb585a9c-4ef7-4b41-b6fb-0c1bbecb03ff.png)



### Installing & Running 

The simulation requires to install [ROS Noetic(which is a set of software libraries and tools that help you build robot applications)](http://wiki.ros.org/noetic/Installation), in particular the _ros-noetic-desktop-full_ integration is raccomended so that all the necessary packages to use Gazebo and Rviz are already available. Moreover, you will require the [slam_gmapping](https://github.com/CarmineD8/slam_gmapping) package.

Another tool to be installed is the xterm interface. We use it to make the user experience more appreciatable, so run this command:
```bash
$ sudo apt-get install -y xterm
```
Once that you've everything ready, Create your workspace and then clone the repository inside src folder of your ROS workspace and build it again. 
Then, launch the package in your terminal by using  following command:

``
$ roslaunch final_assignment.launch
``

The command launches both the files **_simulation_gmapping_** and **_move_base_**, plus the nodes **_teleop_**, **_user_interface_** and **_Assistive_mode _**. In particular, the latter two are the ones that have been specifically developed for the assignment.


### Implimation of the Package 
To satisfy the requirments there  3 different nodes inside the package (USER_INTERFAEC ASSISTIVE & MANUALL) , the simulation enviroment  was provided by the professor, essentially you have to install the slam_gmapping package.

**USER_INTERFACE**
This node represent the iterface of the project to user it communicates with both the node and the user (As shown in above figure ), It get the inputs from the user via terminal and performs the given task.

``
 mode = input('Select a driving mode or press \'q\' to exit: ')


  
    **if (mode == '1'):**
        pub.publish(msg)   %%% If user press the **1** from the keyboard is takes target_position(x & y coordinates) from the user and then publish the msg to (/automatic/cmd_vel)  run the robot in given tirget
        
        
       
   **_autonomous mode_**
   if (mode == '1'):      
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

 
   **_manual mode_** 
   If user press the **2** from the keyboard it enable the teleop_mode and let the user to control the completely 
        elif (mode == '2')
            print('MANUAL MODE\n')            
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

   **_assisted mode_**
   If user press the **3** from the keyboard it enable the Assistive_mode and let the user to control robot and also assist the user to   prevent the robot to smash into walls
   
           elif (mode == '3'):
            print('ASSISTED MODE\n')
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
``


**ASSISTIVE MODE** 
In this node  the collision avidace algorithm is implimented inside the telep_twist_keyboard node that created a new node named assistive node 

`` 
the following method is used in the teleop node  

  **update the linear and angular velocities in order to avoid collisions**
    if regions['front'] > 0.7 and regions['fleft'] > 0.7 and regions['fright'] > 0.7:
        state_description = 'case 1 - no obstacle detected'
    """

    if regions['front'] < 0.7 and regions['fleft'] > 0.7 and regions['fright'] > 0.7:
        state_description = 'case 2 - obstacle in the front'
        # don't go straight
        if (linear_x > 0) and (angular_z == 0):
            linear_x= 0
            angular_z= 0

    elif regions['front'] > 0.7 and regions['fleft'] > 0.7 and regions['fright'] < 0.7:
        state_description = 'case 3 -  obstacle in the fright'
        # don't turn fright
        if (linear_x > 0) and (angular_z < 0):
            linear_x= 0
            angular_z= 0

    elif regions['front'] > 0.7 and regions['fleft'] < 0.7 and regions['fright'] > 0.7:
        state_description = 'case 4 -  obstacle in the fleft'
        # don't turn fleft
        if (linear_x > 0) and (angular_z > 0):
            linear_x= 0
            angular_z= 0

    elif regions['front'] < 0.7 and regions['fleft'] > 0.7 and regions['fright'] < 0.7:
        state_description = 'case 5 - obstacle in the front and fright'
        # don't go straight or turn fright
        if (linear_x > 0) and (angular_z <= 0):
            linear_x= 0
            angular_z= 0

    elif regions['front'] < 0.7 and regions['fleft'] < 0.7 and regions['fright'] > 0.7:
        state_description = 'case 6 -  obstacle in the front and fleft'
        # don't go straight or turn fleft
        if (linear_x > 0) and (angular_z >= 0):
            linear_x= 0
            angular_z= 0

    elif regions['front'] < 0.7 and regions['fleft'] < 0.7 and regions['fright'] < 0.7:
        state_description = 'case 7 -  obstacle in the front and fleft and fright'
        # don't go straight, turn fright or fleft
        if (linear_x > 0):
            linear_x= 0
            angular_z= 0

    elif regions['front'] > 0.7 and regions['fleft'] < 0.7 and regions['fright'] < 0.7:
        state_description = 'case 8 -  obstacle in the fleft and fright'
        # don't turn fright or fleft
        if (linear_x > 0) and (angular_z != 0):
            linear_x= 0
            angular_z= 0

    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

``

The purpose of this node is monitoring the velocity resulting from the user's input and, if necessary, updating it in order to avoid collisions with the external environment. In order to do so, after being initialized, the node subscribes to the following topics:

/manual/cmd_vel: to get the velocity resulting from the user's input;
/scan: to get information about the position of the robot with respect to surrounding obstacles;
Moreover, after having updated the input velocity, the node publishes it on the /assisted/cmd_vel topic.

The real logic of the node is implemented by the utility function avoid_collision, which is in charge of updating the input velocity, when necessary, every time that a new LaserScan message is published on the /scan topic.

### FLOW CHAT
 ![Assignment_3 flow chat](https://user-images.githubusercontent.com/104999107/175319809-35b5946d-35e5-4357-b843-a049b3213371.png)

### rqt_graph
![image](https://user-images.githubusercontent.com/104999107/175324777-710e69f4-d1a4-44ac-b249-0b68df7a3d98.png)
