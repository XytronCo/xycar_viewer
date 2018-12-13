#!/usr/bin/env python
import rospy
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from ackermann_msgs.msg import AckermannDriveStamped

speed = 7.0
steering_angle = 0.1

def set_throttle_steer(data):

    rospy.init_node('servo_commands', anonymous=True)

    pub_vel_left_front_wheel = rospy.Publisher('/xycar/front_left_wheel_velocity_controller/command', Float64, queue_size=1)
    pub_vel_right_front_wheel = rospy.Publisher('/xycar/front_right_wheel_velocity_controller/command', Float64, queue_size=1)

    pub_vel_left_rear_wheel = rospy.Publisher('/xycar/rear_left_wheel_velocity_controller/command', Float64, queue_size=1)
    pub_vel_right_rear_wheel = rospy.Publisher('/xycar/rear_right_wheel_velocity_controller/command', Float64, queue_size=1)


    pub_pos_left_steering_hinge = rospy.Publisher('/xycar/front_left_hinge_position_controller/command', Float64, queue_size=1)
    pub_pos_right_steering_hinge = rospy.Publisher('/xycar/front_right_hinge_position_controller/command', Float64, queue_size=1)

    throttle = data.drive.speed/0.05
    steer = data.drive.steering_angle

    pub_vel_left_rear_wheel.publish(throttle)
    pub_vel_right_rear_wheel.publish(throttle)
    pub_vel_left_front_wheel.publish(throttle)
    pub_vel_right_front_wheel.publish(throttle)
    pub_pos_left_steering_hinge.publish(steer)
    pub_pos_right_steering_hinge.publish(steer)

"""
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub_vel_left_front_wheel.publish(speed)
        pub_vel_right_front_wheel.publish(speed)
        #pub_vel_left_rear_wheel.publish(speed)
        #pub_vel_right_rear_wheel.publish(speed)
        pub_pos_left_steering_hinge.publish(steering_angle)
        pub_pos_right_steering_hinge.publish(steering_angle)
        rate.sleep()
"""
def servo_commands():

    rospy.init_node('servo_commands', anonymous=True)

    rospy.Subscriber("/ackermann_cmd_mux/output", AckermannDriveStamped, set_throttle_steer)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        servo_commands()
    except rospy.ROSInterruptException:
        pass
