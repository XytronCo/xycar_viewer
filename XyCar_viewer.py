#!/usr/bin/env python3

import sys, os, time, threading, subprocess, rospy
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("XyCar_viewer.ui")[0]
form_class_ = uic.loadUiType("wait_please.ui")[0]

class MyWindow(QMainWindow, form_class):

    func = 0

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("XyCar Viewer")
        self.setGeometry(1900,870,210,530)

        self.pushButton_all_ON.clicked.connect(self.all_btn_clicked_on)
        self.pushButton_all_OFF.clicked.connect(self.all_btn_clicked_off)

        self.init_ui(self.pushButton_camera, self.camera_btn_clicked, self.camera_label)
        self.init_ui(self.pushButton_imu, self.imu_btn_clicked, self.IMU_label)
        self.init_ui(self.pushButton_lidar, self.lidar_btn_clicked, self.Lidar_label)
        self.init_ui(self.pushButton_realsense, self.realsense_btn_clicked, self.realsense_label)
        self.init_ui(self.pushButton_xycar, self.xycar_btn_clicked, self.Xycar_Viewer_label)
        
    def init_ui(self, pushButton, btn_clicked, label):
        pushButton.setCheckable(True)
        pushButton.clicked[bool].connect(btn_clicked)
        
        label.setAutoFillBackground(True)
        palette = label.palette()
        palette.setColor(QPalette.Window, QColor(Qt.red))
        label.setPalette(palette)  

    def camera_btn_clicked(self ,pressed):
        package = "usb_cam"
        launch = "usb_cam_remote_view"
        kill_name = "/usb_cam/image_raw" 
   
        if pressed:
            self.btn_clicked(1, package, launch, rkill_name, self.camera_label)
        else: 
            self.btn_clicked(0, package, launch, kill_name, self.camera_label)
           
    def imu_btn_clicked(self, pressed):
        package = "razor_imu_9dof"
        launch = "imu_viwer"
        kill_name = "display_3D_visualization"
  
        if pressed:
            self.btn_clicked(1, package, launch, kill_name, self.IMU_label)
        else: 
            self.btn_clicked(0, package, launch, kill_name, self.IMU_label)
            
        
    def lidar_btn_clicked(self, pressed):
        package = "rplidar_ros"
        launch = "display_lidar"
        kill_name = "rplidar" 

        if pressed:
            self.btn_clicked(1, package, launch, kill_name, self.Lidar_label)
        else: 
            self.btn_clicked(0, package, launch, kill_name, self.Lidar_label)
        
    def realsense_btn_clicked(self, pressed):
        package = "realsense2_camera"
        launch = "display_realsense"
        kill_name = "pointcloud"

        if pressed:
            self.btn_clicked(1, package, launch, kill_name, self.realsense_label)
        else: 
            self.btn_clicked(0, package, launch, kill_name, self.realsense_label)   

    def xycar_btn_clicked(self, pressed):
        package = "xycar_sim"
        launch = "gazebo"
        kill_name = "xycar" 
        
        if pressed:
            self.btn_clicked(1, package, launch, kill_name, self.Xycar_Viewer_label)
        else: 
            self.btn_clicked(0, package, launch, kill_name, self.Xycar_Viewer_label)
            wait = wait_please()
            wait.show()

    def all_btn_clicked_on(self):
        self.pushButton_xycar.setChecked(True)
        self.pushButton_camera.setChecked(True)
        self.pushButton_imu.setChecked(True)
        self.pushButton_lidar.setChecked(True)
        self.pushButton_realsense.setChecked(True)

        self.wait_please(False)
        
        t = threading.Thread(target=self.imu_start)
        self.xycar_btn_clicked(True)
        t.start()

    def imu_start(self):
        t = threading.Thread(target=self.lidar_start)
        rospy.sleep(3)
        self.imu_btn_clicked(True)
        t.start()

    def lidar_start(self):
        t = threading.Thread(target=self.realsense_start)
        rospy.sleep(1)
        self.lidar_btn_clicked(True)
        t.start()

    def realsense_start(self):
        t = threading.Thread(target=self.camera_start)
        rospy.sleep(1)
        self.realsense_btn_clicked(True)
        t.start()

    def camera_start(self):
        rospy.sleep(1)
        self.camera_btn_clicked(True)
        self.wait_please(True)

    def all_btn_clicked_off(self):
        self.pushButton_camera.setChecked(False)
        self.pushButton_imu.setChecked(False)
        self.pushButton_lidar.setChecked(False)
        self.pushButton_realsense.setChecked(False)
        self.pushButton_xycar.setChecked(False)

        self.realsense_btn_clicked(False)
        self.lidar_btn_clicked(False)
        self.imu_btn_clicked(False)
        self.camera_btn_clicked(False)
        self.xycar_btn_clicked(False)
        
        wait = wait_please()
        wait.show()

    def start_node(self, package, launch):
        cmd = "roslaunch " + package + " " + launch + ".launch" + " --pid=~/Desktop/xycar_viewer/pid/" + package + ".pid " + "&"
        os.system(cmd)
        
    def kill_node(self, package):
        cmd = "kill -2 `cat ./pid/" + package + ".pid`"
        os.system(cmd)
        os.system("kill -2 `cat ./pid/" + package + ".pid`")

    def wait_please(self, switch):
        self.pushButton_camera.setEnabled(switch)
        self.pushButton_imu.setEnabled(switch)
        self.pushButton_lidar.setEnabled(switch)
        self.pushButton_realsense.setEnabled(switch)
        self.pushButton_xycar.setEnabled(switch)
        self.pushButton_all_ON.setEnabled(switch)
        self.pushButton_all_OFF.setEnabled(switch)

    def btn_clicked(self ,pressed, package, launch, kill_name, label):
        if pressed:
            self.start_node(package, launch)

            delay_list = []
            delay_list.append(kill_name)

            if delay_list[0] == "xycar":
                delay_list.append("gzserver")
                delay_list.append("gzclient")
                delay_list.append("spawner")
                delay_list.append("robot_state_publisher")
                delay_list.append("xycar.rviz")
                delay_list.append("test_command")

            for i in range(0,len(delay_list)):
                while True:
                    result = subprocess.Popen(['ps','-ef'],stdout=subprocess.PIPE)
                    stdout = result.communicate()         
                    index = str(stdout).find(delay_list[i])

                    if index != -1:
                        break

            delay_list = []

            palette = label.palette()
            palette.setColor(QPalette.Window, QColor(Qt.blue))
            label.setPalette(palette) 

        else: 
            self.kill_node(package)

            palette = label.palette()
            palette.setColor(QPalette.Window, QColor(Qt.red))
            label.setPalette(palette) 

class wait_please(QDialog, form_class_):

    def __init__(self):
        super(wait_please, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Wait Please")
        self.setGeometry(1750,770,223,66)

        self.setModal(True)
        t = threading.Thread(target=self.delay)
        t.start()
    
    def delay(self):
        t = threading.Thread(target=self.visual_time)
        t.start()
        rospy.sleep(16)

    def visual_time(self):
        count = 15
        while True:
            if count == 0:
                break
            rospy.sleep(1)
            count-=1
            self.number.setText(str(count))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
