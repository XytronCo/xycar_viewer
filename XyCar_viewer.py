#!/usr/bin/env python3

import sys, os, time, threading, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("XyCar_viewer.ui")[0]

class MyWindow(QMainWindow, form_class):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

        self.create_exit_sh()

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
        rviz = 0
        kill_name = "/usb_cam/image_raw" 
        move_name = {kill_name:'0,0,100,100'}
   
        if pressed:
            self.btn_clicked(1, package, launch, rviz, kill_name, move_name, self.camera_label)
        else: 
            self.btn_clicked(0, package, launch, rviz, kill_name, move_name, self.camera_label)
           
    def imu_btn_clicked(self, pressed):
        package = "razor_imu_9dof"
        launch = "imu_viwer"
        rviz = 0
        kill_name = "display_3D_visualization_node"
        move_name = {
            '9DOF Razor IMU Main Screen':'0,595,100,100',
            '9DOF Razor IMU Roll, Pitch, Yaw':'500,595,100,100'
        }
  
        if pressed:
            self.btn_clicked(1, package, launch, rviz, kill_name, move_name, self.IMU_label)
        else: 
            self.btn_clicked(0, package, launch, rviz, kill_name, move_name, self.IMU_label)
            
        
    def lidar_btn_clicked(self, pressed):
        package = "rplidar_ros"
        launch = "display_lidar"
        rviz = 1
        kill_name = "rplidar" 
        move_name = {kill_name:'710,0,600,520'}

        if pressed:
            self.btn_clicked(1, package, launch, rviz, kill_name, move_name, self.Lidar_label)
        else: 
            self.btn_clicked(0, package, launch, rviz, kill_name, move_name, self.Lidar_label)
        
    def realsense_btn_clicked(self, pressed):
        package = "realsense2_camera"
        launch = "demo_pointcloud"
        rviz = 1
        kill_name = "pointcloud"
        move_name = {kill_name:'1320,0,600,520'}

        if pressed:
            self.btn_clicked(1, package, launch, rviz, kill_name, move_name, self.realsense_label)
        else: 
            self.btn_clicked(0, package, launch, rviz, kill_name, move_name, self.realsense_label)   

    def xycar_btn_clicked(self, pressed):
        package = "xycar_sim"
        launch = "gazebo"
        rviz = 1
        kill_name = "xycar" 
        move_name = {kill_name:'960,598,400,480'}
        
        if pressed:
            self.btn_clicked(1, package, launch, rviz, kill_name, move_name, self.Xycar_Viewer_label)
            #self.kill_node("gazebo")
        else: 
            self.btn_clicked(0, package, launch, rviz, kill_name, move_name, self.Xycar_Viewer_label)
            self.Xycar_exit()
            self.daegi(7)

    def all_btn_clicked_on(self):
        self.pushButton_xycar.setChecked(True)
        self.pushButton_camera.setChecked(True)
        self.pushButton_imu.setChecked(True)
        self.pushButton_lidar.setChecked(True)
        self.pushButton_realsense.setChecked(True)

        self.wait_please(True)
        self.xycar_btn_clicked(True)
        time.sleep(3)
        self.imu_btn_clicked(True)
        time.sleep(1)
        self.lidar_btn_clicked(True)
        time.sleep(1)
        self.realsense_btn_clicked(True)
        time.sleep(1)
        self.camera_btn_clicked(True)
        self.wait_please(False) 

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
        self.Xycar_exit()
        self.daegi(7)

    def daegi(self, timer):
        t = threading.Thread(target=self.Xy_sleep, args=(timer,))
        self.wait_please(False)
        t.start()

    def daegi_move_window(self, timer, dic_key, move_name, rviz):
        t = threading.Thread(target=self.Xy_sleep_move_window, args=(timer, dic_key, move_name, rviz,))
        self.wait_please(False)
        t.start()

    def Xy_sleep(self, timer):
        time.sleep(timer)
        self.wait_please(True)

    def Xy_sleep_move_window(self, timer, dic_key, move_name, rviz):
        time.sleep(timer)
        for i in range(0,len(dic_key)):
            self.move_window(dic_key[i],move_name[dic_key[i]],rviz)
        self.wait_please(True)

    def Xycar_exit(self):
        self.kill_node("gzserver")
        self.kill_node("gazebo")
        self.kill_node("xycar_sim")
        self.kill_node("controller_manager")
        self.kill_node("robot_state_publisher")
        
    def create_exit_sh(self):
        exit_sh = [
            'a=""\n',
            'while [ True ]; do\n',
	        'a=$(echo `ps -ef | grep $1 | grep -v "grep"` | cut -d " " -f2)\n',
	        'if [ "$a" = "" ]; then\n',
		    'break\n',
	        'else\n',
		    'kill -9 $a\n',
		    'a=""\n',
		    'fi\n',
            'done\n'
        ]

        f = open("./exit.sh", "w")
        for i in exit_sh:
            f.write(i)
        f.close()

        os.system("chmod +x ./exit.sh")

    def start_node(self, package, launch, rviz):
        cmd = "roslaunch " + package + " " + launch + ".launch" + " " + "&"
        os.system(cmd)

    def move_window(self, name, geometry, rviz):
        cmd = []

        if rviz == 1:  
            name = name + ".rviz"            
            cmd.append("wmctrl -r '" + name + "* - RViz' -e '0," + geometry + "'")
            cmd.append("wmctrl -r '" + name + " - RViz' -e '0," + geometry + "'")
        else:
            cmd.append("wmctrl -r '" + name + "' -e '0," + geometry + "'")

        for i in cmd:    
            os.system(i)
        
    def kill_node(self, name):
        cmd = "./exit.sh " + name
        os.system(cmd)

    def wait_please(self, switch):
        self.pushButton_camera.setEnabled(switch)
        self.pushButton_imu.setEnabled(switch)
        self.pushButton_lidar.setEnabled(switch)
        self.pushButton_realsense.setEnabled(switch)
        self.pushButton_xycar.setEnabled(switch)
        self.pushButton_all_ON.setEnabled(switch)
        self.pushButton_all_OFF.setEnabled(switch)

    def btn_clicked(self ,pressed, package, launch, rviz, kill_name, move_name, label):
        dic_key = []
        xycar = 0
        for key in move_name.keys():
            dic_key.append(key)

        if rviz == 1:
            kill_name = kill_name + ".rviz"

        if pressed:
            palette = label.palette()
            palette.setColor(QPalette.Window, QColor(Qt.blue))
            label.setPalette(palette) 

            self.start_node(package, launch, rviz)

            delay_name = kill_name.replace("/","_")
            file_name = "./proc_name_" + delay_name
            
            delay_list = []
            delay_list.append(delay_name)

            if kill_name == "xycar":
                delay_list.append("gzserver")
                delay_list.append("gazebo")
                delay_list.append("xycar_sim")
                delay_list.append("controller_manager")
                delay_list.append("robot_state_publisher")
                xycar = 1
            elif kill_name == "/usb_cam/image_raw":
                delay_list[0] = "/usb_cam/image_raw"

            for i in range(0,len(delay_list)):
                while True:
                    result = subprocess.Popen(['ps','-ef'],stdout=subprocess.PIPE)
                    stdout = result.communicate()         
                    index = str(stdout).find(delay_list[i])

                    if index == -1:
                        continue
                    else:
                        if xycar == 0:
                            self.daegi_move_window(3, dic_key, move_name, rviz)
                        break

            delay_list = []

        else: 
            palette = label.palette()
            palette.setColor(QPalette.Window, QColor(Qt.red))
            label.setPalette(palette) 
            
            self.kill_node(kill_name)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

    os.system("rm -rf ./exit.sh")
