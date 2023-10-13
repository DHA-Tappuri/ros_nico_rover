#!/usr/bin/env python3
# coding: utf-8

import os, time
from PCA9685 import PCA9685


# motor driver
class motor_driver(object):
    # constructor
    def __init__(self):
        # PCA9685
        self._pwm = PCA9685( address=0x40 ,debug=False )
        self._pwm.setPWMFreq(10000)
        # motor A
        self._motA_pwm = 0
        self._motA_in1 = 1
        self._motA_in2 = 2
        # motor B
        self._motB_pwm = 5
        self._motB_in1 = 3
        self._motB_in2 = 4


    # destructor
    def __del__(self):
        pass


    # drive motor
    def drive(self, index, speed):
        _speed = 0
        _dir   = 0

        # speed and direction check
        if(   speed > 0 ):
            _speed =  speed
            _dir   =  1
        elif( speed < 0 ):
            _speed = -speed
            _dir   = -1

        # limit check
        if( _speed > 100 ):
            _speed = 100

        # motor
        if(index == 0):
            # motor A
            self._pwm.setDutycycle( self._motA_pwm, _speed )
            if(_dir == 1):
                # CCW
                self._pwm.setLevel( self._motA_in1, 0 )
                self._pwm.setLevel( self._motA_in2, 1 )
            elif(_dir == -1):
                # CW
                self._pwm.setLevel( self._motA_in1, 1 )
                self._pwm.setLevel( self._motA_in2, 0 )
            else:
                # stop(brake)
                self._pwm.setLevel( self._motA_in1, 0 )
                self._pwm.setLevel( self._motA_in2, 0 )
        else:
            # motor B
            self._pwm.setDutycycle( self._motB_pwm, _speed )
            if(_dir == 1):
                # CCW
                self._pwm.setLevel( self._motB_in1, 0 )
                self._pwm.setLevel( self._motB_in2, 1 )
            elif(_dir == -1):
                # CW
                self._pwm.setLevel( self._motB_in1, 1 )
                self._pwm.setLevel( self._motB_in2, 0 )
            else:
                # stop(brake)
                self._pwm.setLevel( self._motB_in1, 0 )
                self._pwm.setLevel( self._motB_in2, 0 )


    # stop motor
    def stop(self, index):
        if (index == 0):
            self._pwm.setDutycycle( self._motA_pwm, 0 )
        else:
            self._pwm.setDutycycle( self._motB_pwm, 0 )




# main function
if( __name__ == '__main__' ):
    print("this is a motor driver test code")
    drv = motor_driver()

    print("forward 2 s")
    drv.drive(0, 15)
    drv.drive(1, 15)
    time.sleep(2)

    print("backward 2 s")
    drv.drive(0, -15)
    drv.drive(1, -15)
    time.sleep(2)

    print("stop")
    drv.stop(0)
    drv.stop(1)


