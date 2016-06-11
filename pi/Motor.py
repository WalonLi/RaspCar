#!/usr/bin/python3

"""
author : Walon Li
"""

"""
3           2
    car
1           4
"""

import RPi.GPIO as GPIO
import time

class Motor():

    motor_1a = 3
    motor_1b = 6
    motor_2a = 1
    motor_2b = 7
    motor_3a = 5
    motor_3b = 4
    motor_4a = 0
    motor_4b = 2

    forward_byte    = 0x2b
    left_byte       = 0x53

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
        #GPIO.output(self._gpio_map["PWM1"], GPIO.HIGH)
        #GPIO.output(self._gpio_map["PWM2"], GPIO.HIGH)
        #GPIO.output(self._gpio_map["PWM3"], GPIO.HIGH)
        #GPIO.output(self._gpio_map["PWM4"], GPIO.HIGH)

        # set PWM
        p1 = GPIO.PWM(self._gpio_map["PWM1"], 255)
        p2 = GPIO.PWM(self._gpio_map["PWM2"], 255)
        p3 = GPIO.PWM(self._gpio_map["PWM3"], 255)
        p4 = GPIO.PWM(self._gpio_map["PWM4"], 255)
        self._pwm_map = [p1, p2, p3, p4]
        for i in self._pwm_map:
            i.start(100)

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
        #time.sleep(5)

    def backward(self):
        for i in self._pwm_map:
            i.ChangeDutyCycle(100)

        self._motoLatch(Motor.forward_byte ^ 0xff)
        #time.sleep(5)


    def turnLeft(self):
        for i in self._pwm_map:
            i.ChangeDutyCycle(100)

        self._motoLatch(Motor.left_byte)
        #time.sleep(5)

    def turnRight(self):
        for i in self._pwm_map:
            i.ChangeDutyCycle(100)

        self._motoLatch(Motor.left_byte ^ 0xff)
        #time.sleep(2)


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

