#!/usr/bin/env python3
# coding: utf-8

import os, time
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg   import Joy
from driver           import motor_driver

# initialize variables
_driver       = None     # motor driver
_wheel_radius = 0.06     # [m] wheel radius
_wheel_tread  = 0.10     # [m] wheel tread
_gear_rate    = 48.6     # [-] gear rate
_voltage      = 9.0      # [V] battery voltage
_rpm_to_volt  = 0.001  # [V/rpm] rate between voltage and RPM



# control rover
def _control_rover( trans_vel=0.0, rot_vel=0.0 ):
    global _driver
    global _wheel_radius, _wheel_tread
    global _gear_rate, _battery_voltage

    ( _trans_ms, _rot_rads ) = ( trans_vel, rot_vel )
    ( _rpm_l,    _rpm_r    ) = ( 0, 0 )
    ( _duty_l,   _duty_r   ) = ( 0, 0 )
    # wheel RPM
    _rpm_l    = ( _trans_ms - _rot_rads * _wheel_tread * 0.5 ) * 60.0 / ( _wheel_radius * 3.141592 ) * _gear_rate
    _rpm_r    = ( _trans_ms + _rot_rads * _wheel_tread * 0.5 ) * 60.0 / ( _wheel_radius * 3.141592 ) * _gear_rate
    # duty rate
    _duty_l   = _rpm_l * _rpm_to_volt / _voltage * 100.0
    _duty_r   = _rpm_r * _rpm_to_volt / _voltage * 100.0

    print( _duty_l, _duty_r )

    # command
    _driver.drive(1,  _duty_l)
    _driver.drive(0, -_duty_r)


# callback function
def _callback_joy( msg ):
    if( msg.buttons[0] ):
        _control_rover( trans_vel=msg.axes[1]*0.15, rot_vel=msg.axes[0]*1.5 )
    else:
        _control_rover()
    return



# callback function
def _callback_cmd_vel( msg ):
    _control_rover( trans_vel=msg.linear.x, rot_vel=msg.angular.z )
    return




# main function
if( __name__ == '__main__' ):
    try:
        # initialize node
        rospy.init_node( 'nico_rover', anonymous = True )

        # load parameters

        # initialize topics
        _sub_cmd_vel = rospy.Subscriber( 'cmd_vel', Twist, _callback_cmd_vel )
        _sub_joy     = rospy.Subscriber( 'joy',     Joy,   _callback_joy     )

        # initialize motor driver
        _driver = motor_driver()

        # start
        rospy.spin()

    except rospy.ROSInterruptException:
        _driver.stop(0)
        _driver.stop(1)
        print('exit.')

