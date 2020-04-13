# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from std_srvs.srv import Trigger
import rclpy
import RPi.GPIO as GPIO # Import the GPIO Library
import time # Import the Time library


g_node = None


def triggerMotor(request, response):
    global g_node

    g_node.get_logger().info('Trigger Motor!')
     # enable motors
    GPIO.output(11, 1)
    GPIO.output(22, 1)
    
    # Turn the right motor forwards
    GPIO.output(27, 0)
    GPIO.output(17, 1)

    # Turn the left motor forwards
    GPIO.output(10, 0)
    GPIO.output(9, 1)
    # Wait for 1 seconds
    time.sleep(1)

    # Turn all motors off
    GPIO.output(11, 0)
    GPIO.output(10, 0)
    GPIO.output(9, 0)
    GPIO.output(22, 0)
    GPIO.output(27, 0)
    GPIO.output(17, 0)

    response.success = True
    response.message = "Sucess!"

    return response


def main(args=None):
    global g_node
    rclpy.init(args=args)

    # Set the GPIO modes
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # Set the GPIO Pin mode
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(10, GPIO.OUT)
    GPIO.setup(9, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(17, GPIO.OUT)
    
    # Turn all motors off
    GPIO.output(11, 0)
    GPIO.output(10, 0)
    GPIO.output(9, 0)
    GPIO.output(22, 0)
    GPIO.output(27, 0)
    GPIO.output(17, 0)

    g_node = rclpy.create_node('motor')

    srv = g_node.create_service(Trigger, 'triggerMotor', triggerMotor)
    while rclpy.ok():
        rclpy.spin_once(g_node)

    # Reset the GPIO pins (turns off motors too)
    GPIO.cleanup()

    # Destroy the service attached to the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    g_node.destroy_service(srv)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
