#!/usr/bin/python3

"""
GNU GENERAL PUBLIC LICENSE
Copyright (C) 2015  WalonLi
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import RPi.GPIO as GPIO
import time

class Motor():
    motor_1a = 0b10
    motor_1b = 0b11
    motor_2a = 0b1
    motor_2b = 0b100
    motor_3a = 0b101
    motor_3b = 0b111
    motor_4a = 0b0
    motor_4b = 0b110

    forward_byte = 0x2b


    def __init__(self):

        self._gpio_map = {"PWM2":37, "DIR_CLK":38, "PWM3":35, "PWM4":36, "DIR_EN":33,
                         "DIR_UP":31, "PWM1":32, "DIR_LATCH":29}
        self._pwm_map = []

        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)

        # set GPIO OUT mode
        for i in iter(self._gpio_map):
            GPIO.setup(self._gpio_map[i], GPIO.OUT)

        # set PWM
        GPIO.output(self._gpio_map["PWM1"], GPIO.HIGH)
        GPIO.output(self._gpio_map["PWM2"], GPIO.HIGH)
        GPIO.output(self._gpio_map["PWM3"], GPIO.HIGH)
        GPIO.output(self._gpio_map["PWM4"], GPIO.HIGH)

        # set PWM
        p1 = GPIO.PWM(self._gpio_map["PWM1"], 250)
        p2 = GPIO.PWM(self._gpio_map["PWM2"], 250)
        p3 = GPIO.PWM(self._gpio_map["PWM3"], 250)
        p4 = GPIO.PWM(self._gpio_map["PWM4"], 250)
        self._pwm_map = [p1, p2, p3, p4]
        for i in self._pwm_map:
            i.start(0)

    def __del__(self):
        GPIO.output(self._gpio_map["PWM1"], GPIO.LOW)
        GPIO.output(self._gpio_map["PWM2"], GPIO.LOW)
        GPIO.output(self._gpio_map["PWM3"], GPIO.LOW)
        GPIO.output(self._gpio_map["PWM4"], GPIO.LOW)
        self._motoLatch(0)
        GPIO.cleanup()

    def stop(self):
        for i in self._pwm_map:
            i.ChangeDutyCycle(0)
        self._motoLatch(0)

    def forward(self):
        for i in self._pwm_map:
            i.ChangeDutyCycle(100)

        self._motoLatch(Motor.forward_byte)
        time.sleep(5)

    def backward(self):
        for i in self._pwm_map:
            i.ChangeDutyCycle(100)

        self._motoLatch(Motor.forward_byte ^ 0xff)
        time.sleep(5)


    def turnLeft(self):
        self._pwm_map[0].ChangeDutyCycle(0)
        self._pwm_map[1].ChangeDutyCycle(0)
        self._pwm_map[2].ChangeDutyCycle(100)
        self._pwm_map[3].ChangeDutyCycle(100)

        self._motoLatch(Motor.forward_byte)
        time.sleep(5)

    def turnRight(self):
        self._pwm_map[0].ChangeDutyCycle(100)
        self._pwm_map[1].ChangeDutyCycle(100)
        self._pwm_map[2].ChangeDutyCycle(0)
        self._pwm_map[3].ChangeDutyCycle(0)

        self._motoLatch(Motor.forward_byte)
        time.sleep(2)
        pass


    # inner function, don't call it directly
    def _motoLatch(self, v):
        GPIO.output(self._gpio_map["DIR_LATCH"], GPIO.LOW)

        for i in range(8):
            GPIO.output(self._gpio_map["DIR_CLK"], GPIO.LOW)

            if v & 0x1:
                GPIO.output(self._gpio_map["DIR_UP"], GPIO.HIGH)
            else:
                GPIO.output(self._gpio_map["DIR_UP"], GPIO.LOW)
            v >>= 1
            GPIO.output(self._gpio_map["DIR_CLK"], GPIO.HIGH)

        GPIO.output(self._gpio_map["DIR_LATCH"], GPIO.HIGH)

