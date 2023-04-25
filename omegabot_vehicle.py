import smbus
import time
import threading

forward = 0x00
backward = 0x01

class omegabotVehicle(object):

    directionFirstWheel = 0x04
    speedFirstWheel = 0x05
    directionSecondWheel = 0x06
    speedSecondWheel = 0x07
    stopMotors = 0x08

    def __init__(self, slaveAddr = 0x27, beginSpeed = 0, beginDirection = 0):
        self.slaveAddr = slaveAddr
        self.speed = beginSpeed
        self.direction = beginDirection
        self.bus = smbus.SMBus(1)
    #     self.timer = time.time()
    #     self.event = threading.Event()
    #
    # def check_state(self):
    #     if self.timer - time.time() == 2 and

    def set_speed(self, wheel, speed):
        with self.bus as b:
            try:
                b.write_byte_data(self.slaveAddr, wheel, speed)
            except Exception as e:
                print(e)
                return False
        return True

    def set_direction(self, wheel, direction):
        with self.bus as b:
            try:
                b.write_byte_data(self.slaveAddr, wheel, direction)
            except Exception as e:
                print(e)
                return False
        return True

    def move_forward(self, speed=150):
        if not self.set_direction(omegabotVehicle.directionFirstWheel, forward) \
                and not self.set_direction(omegabotVehicle.directionSecondWheel, forward) \
                and not self.set_speed(omegabotVehicle.speedFirstWheel, speed) \
                and not self.set_speed(omegabotVehicle.speedSecondWheel, speed):
            return False
        return True

    def move_backward(self, speed=150):
        if not self.set_direction(omegabotVehicle.directionFirstWheel, backward) \
                and not self.set_direction(omegabotVehicle.directionSecondWheel, backward) \
                and not self.set_speed(omegabotVehicle.speedFirstWheel, 255 - speed) \
                and not self.set_speed(omegabotVehicle.speedSecondWheel, 255 - speed):
            return False
        return True

    def stop_motors(self):
        if not self.set_direction(omegabotVehicle.directionFirstWheel, forward) \
            and not self.set_direction(omegabotVehicle.directionSecondWheel, forward) \
            and not self.set_speed(omegabotVehicle.speedFirstWheel, 0) \
            and not self.set_speed(omegabotVehicle.speedSecondWheel, 0):
            return False
        return True


    # def rotate(self, angle):