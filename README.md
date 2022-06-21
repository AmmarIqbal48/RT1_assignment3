# RT1_Assignment3 

Made by **ammar Iqbal**

Student ID :** ------**

**Introduction**  

This is the third Assignment of the corse Research_Track_1 in this Assignment  we asked  to create architecture on ROS and its softwear capable of controlling a mobile robot in given enviroment along with  creating a multiple modes for the user in  which  user allow to choose how to control the robot.

**_FOLLOWING ARE THE MODE_**


* --> **TO DRIVE THE ROBOT AUTONOMOUSLY**: This Mode ask the user to set the position and than robot will go to that position by itself with avoiding the obsticals
            
* --> **TO DRIVE THE ROBOT MANUALLY**:In this mode  robot is completely operated by the user manually by using the keyboard. 
            
* --> **TO DRIVE THE ROBOT MANUALLY WITH ASSISTIVE MODE**: In this mode robot is operated by the user manually by using the keyboard but this also assist the user to   prevent the robot to smash into walls 
 
 **USER_INTERFACE**
![image](https://user-images.githubusercontent.com/104999107/174690203-eb585a9c-4ef7-4b41-b6fb-0c1bbecb03ff.png)



### INSTALLING 

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

