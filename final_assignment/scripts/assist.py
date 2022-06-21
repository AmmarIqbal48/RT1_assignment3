#!/usr/bin/env python

from __future__ import print_function

import threading

import roslib; roslib.load_manifest('teleop_twist_keyboard')
import rospy

from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan

import sys, select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty

# global variables
pubb= None               # publisher to /cmd_vel topic
astd_vel= Twist()       # velocity message where to save the updated velocity

# Callbacks
'''
    Function that is called each time that a new message on the /scan topic is
    published. It divides the ranges vector into five regions in order to get the
    minimum value in each and give this as input to the collision avoidance function.
        Args:
          - msg: LaserScan message that contains the ranges returned by the sensor;
        Return:
          - void
'''
def scan_callback(msg):
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:719]), 10),
    }

    avoid_collision(regions)

'''
    Function that is called each time that a new message on the /manual/cmd_vel
    topic is published. The function is used to copy such message in another one
    of the same type to be published on the /assisted/cmd_vel topic.
      Args:
        - msg: Twist message that contains the velocity generated by the teleop_twist_keyboard node;
      Return:
        - void
'''
def astd_vel_callback(msg):
    global astd_vel
    astd_vel= msg


# Utility functions
'''
    Function that is used to implement the collision avoidance mechanism. It checks
    the distances of the robot from the external environment and updates its velocity
    in order to avoid collisions.
        Args:
          - regions: a collection that contains the minimum distances in 5 direction;
        Return:
          - void
'''
def avoid_collision(regions):
    global astd_vel
    global pubb
    # save the current linear and angular velocities obtained as the result of the
    # user's keyboard input
    linear_x= astd_vel.linear.x
    angular_z= astd_vel.angular.z

    state_description = ''
    """
    # update the linear and angular velocities in order to avoid collisions
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

    # update the  linear and angular velocities
    astd_vel.linear.x= linear_x
    astd_vel.angular.z= angular_z

    # display the obstacle's state
    # rospy.loginfo(state_description)
    # publish the modified velocity on /assisted/cmd_vel
    pubb.publish(astd_vel)


TwistMsg = Twist

msg = """
Reading from the keyboard  and Publishing to Twist!
---------------------------
Moving around:
   u    i    o
   j    k    l
   m    ,    .

For Holonomic mode (strafing), hold down the shift key:
---------------------------
   U    I    O
   J    K    L
   M    <    >

t : up (+z)
b : down (-z)

anything else : stop

q/z : increase/decrease max speeds by 10%
w/x : increase/decrease only linear speed by 10%
e/c : increase/decrease only angular speed by 10%

CTRL-C to quit
"""

moveBindings = {
        'i':(1,0,0,0),
        'o':(1,0,0,-1),
        'j':(0,0,0,1),
        'l':(0,0,0,-1),
        'u':(1,0,0,1),
        ',':(-1,0,0,0),
        '.':(-1,0,0,1),
        'm':(-1,0,0,-1),
        'O':(1,-1,0,0),
        'I':(1,0,0,0),
        'J':(0,1,0,0),
        'L':(0,-1,0,0),
        'U':(1,1,0,0),
        '<':(-1,0,0,0),
        '>':(-1,-1,0,0),
        'M':(-1,1,0,0),
        't':(0,0,1,0),
        'b':(0,0,-1,0),
    }

speedBindings={
        'q':(1.1,1.1),
        'z':(.9,.9),
        'w':(1.1,1),
        'x':(.9,1),
        'e':(1,1.1),
        'c':(1,.9),
    }

class PublishThread(threading.Thread):
    def __init__(self, rate):
        super(PublishThread, self).__init__()
        self.publisher = rospy.Publisher('cmd_vel', TwistMsg, queue_size = 1)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0
        self.speed = 0.0
        self.turn = 0.0
        self.condition = threading.Condition()
        self.done = False

        # Set timeout to None if rate is 0 (causes new_message to wait forever
        # for new data to publish)
        if rate != 0.0:
            self.timeout = 1.0 / rate
        else:
            self.timeout = None

        self.start()

    def wait_for_subscribers(self):
        i = 0
        while not rospy.is_shutdown() and self.publisher.get_num_connections() == 0:
            if i == 4:
                print("Waiting for subscriber to connect to {}".format(self.publisher.name))
            rospy.sleep(0.5)
            i += 1
            i = i % 5
        if rospy.is_shutdown():
            raise Exception("Got shutdown request before subscribers connected")

    def update(self, x, y, z, th, speed, turn):
        self.condition.acquire()
        self.x = x
        self.y = y
        self.z = z
        self.th = th
        self.speed = speed
        self.turn = turn
        # Notify publish thread that we have a new message.
        self.condition.notify()
        self.condition.release()

    def stop(self):
        self.done = True
        self.update(0, 0, 0, 0, 0, 0)
        self.join()

    def run(self):
        twist_msg = TwistMsg()

        if stamped:
            twist = twist_msg.twist
            twist_msg.header.stamp = rospy.Time.now()
            twist_msg.header.frame_id = twist_frame
        else:
            twist = twist_msg
        while not self.done:
            if stamped:
                twist_msg.header.stamp = rospy.Time.now()
            self.condition.acquire()
            # Wait for a new message or timeout.
            self.condition.wait(self.timeout)

            # Copy state into twist message.
            twist.linear.x = self.x * self.speed
            twist.linear.y = self.y * self.speed
            twist.linear.z = self.z * self.speed
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = self.th * self.turn

            self.condition.release()

            # Publish.
            self.publisher.publish(twist_msg)

        # Publish stop message when thread exits.
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0
        self.publisher.publish(twist_msg)


def getKey(settings):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)

def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":

      # initialize the node
    rospy.init_node('collision_avoidance')

    # define a publisher to the /assisted/cmd_vel topic

    pubb = rospy.Publisher('/assisted/cmd_vel', Twist, queue_size= 1)

    # define a subscriber to the /scan topic
    sub1= rospy.Subscriber('/scan', LaserScan, scan_callback)

    # define a subscriber to the /manual/cmd_vel topic
    sub2= rospy.Subscriber('/manual/cmd_vel', Twist, astd_vel_callback)

    settings = saveTerminalSettings()

    speed = rospy.get_param("~speed", 0.5)
    turn = rospy.get_param("~turn", 1.0)
    repeat = rospy.get_param("~repeat_rate", 0.0)
    key_timeout = rospy.get_param("~key_timeout", 0.0)
    stamped = rospy.get_param("~stamped", False)
    twist_frame = rospy.get_param("~frame_id", '')
    if stamped:
        TwistMsg = TwistStamped
    if key_timeout == 0.0:
        key_timeout = None

    pub_thread = PublishThread(repeat)

    x = 0
    y = 0
    z = 0
    th = 0
    status = 0

    try:
        pub_thread.wait_for_subscribers()
        pub_thread.update(x, y, z, th, speed, turn)

        print(msg)
        print(vels(speed,turn))
        while(1):
            key = getKey(settings)
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                y = moveBindings[key][1]
                z = moveBindings[key][2]
                th = moveBindings[key][3]
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]

                print(vels(speed,turn))
                if (status == 14):
                    print(msg)
                status = (status + 1) % 15
            else:
                # Skip updating cmd_vel if key timeout and robot already
                # stopped.
                if key == '' and x == 0 and y == 0 and z == 0 and th == 0:
                    continue
                x = 0
                y = 0
                z = 0
                th = 0
                if (key == '\x03'):
                    break
 
            pub_thread.update(x, y, z, th, speed, turn)

    except Exception as e:
        print(e)

    finally:
        pub_thread.stop()
        restoreTerminalSettings(settings)
