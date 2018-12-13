현재 위치의 파일들을 모두 아래 지정된 위치 안에 넣습니다.  



display_3D_visualization.py : ~/xycar/src/razor_imu_9dof/nodes/  

pointcloud.rviz  :  ~/xycar/src/realsense2_camera/rviz/  

rplidar.rviz     :  ~/xycar/src/rplidar_ros/rviz/  

xycar.rviz       :  ~/xycar/src/xycar_sim/rviz/  

gui.ini          :  ~/.gazebo  



gazebo의 경우 다음 패키지를 반드시 설치합니다.

sudo apt-get install ros-kinetic-gazebo-ros-control  
sudo apt-get install ros-kinetic-joint-state-controller  
sudo apt-get install ros-kinetic-effort-controllers  
sudo apt-get install ros-kinetic-position-controllers  