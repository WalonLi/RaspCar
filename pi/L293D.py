#!/usr/bin/python3
#Walon

import RPi.GPIO as GPIO
import time




def latch_(d, value):
    #GPIO.output(d["DIR_UP"], GPIO.LOW)
    GPIO.output(d["DIR_LATCH"], GPIO.LOW)


    for i in range(8):
        GPIO.output(d["DIR_CLK"], GPIO.LOW)
        if value & 0x1:
            GPIO.output(d["DIR_UP"], GPIO.HIGH)
        else:
            GPIO.output(d["DIR_UP"], GPIO.LOW)
        value >>= 1
        """
        if i % 2 == 1 and value == 1:
            GPIO.output(d["DIR_UP"], GPIO.HIGH)
            print(d["DIR_UP"], i)
        else:
            GPIO.output(d["DIR_UP"], GPIO.LOW)
            print("LOW", i)
        """
        GPIO.output(d["DIR_CLK"], GPIO.HIGH)

    GPIO.output(d["DIR_LATCH"], GPIO.HIGH)




print("L293D Test start")

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

GpIO_Dict = {"PWM2":37, "DIR_CLK":38, "PWM3":35, "PWM4":36, "DIR_EN":33,
             "DIR_UP":31, "PWM1":32, "DIR_LATCH":29}


for i in iter(GpIO_Dict):
    print(i, GpIO_Dict[i])
    GPIO.setup(GpIO_Dict[i], GPIO.OUT)


GPIO.output(GpIO_Dict["PWM1"], GPIO.HIGH)
GPIO.output(GpIO_Dict["PWM2"], GPIO.HIGH)
GPIO.output(GpIO_Dict["PWM3"], GPIO.HIGH)
GPIO.output(GpIO_Dict["PWM4"], GPIO.HIGH)

#p1 = GPIO.PWM(GpIO_Dict["PWM1"], 250)
#p1.start(0)
#p1.ChangeDutyCycle(50)



#latch_(GpIO_Dict, 0)
#time.sleep(3)

#GPIO.output(d["DIR_CLK"], GPIO.LOW)
#GPIO.output(GpIO_Dict["DIR_EN"], GPIO.HIGH)
GPIO.output(GpIO_Dict["DIR_EN"], GPIO.LOW)

#reset
latch_(GpIO_Dict, 0)

"""
#define MOTOR1_A 2
#define MOTOR1_B 3
#define MOTOR2_A 1
#define MOTOR2_B 4
#define MOTOR4_A 0
#define MOTOR4_B 6
#define MOTOR3_A 5
#define MOTOR3_B 7
"""
#0 0 1 0 1 0 1 1
latch_(GpIO_Dict, 0x2b)

#GPIO.output(GpIO_Dict["PWM1"], GPIO.HIGH)
time.sleep(2)

GPIO.output(GpIO_Dict["PWM1"], GPIO.LOW)
GPIO.output(GpIO_Dict["PWM2"], GPIO.LOW)
GPIO.output(GpIO_Dict["PWM3"], GPIO.LOW)
GPIO.output(GpIO_Dict["PWM4"], GPIO.LOW)


time.sleep(1)
GPIO.cleanup()

