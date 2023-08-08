#include "../include/qt_cirlab_monitor/qnode.hpp"
#include <sstream>
#include <string.h>
#include <iostream>
#include <sys/socket.h>


/*
    This cpp file allows you to use the publish and subscribe functions of ROS.
*/

namespace monitor
{
    QNode::~QNode() {
          if (ros::isStarted())
          {
            ros::shutdown();    // explicitly needed since we use ros::start();
            ros::waitForShutdown();
          }
          wait();
}

bool QNode::init()
{
    start();
    return true;
}

void QNode::run()
{
    ros::Rate r(30);
    while(ros::ok())
    {
        ros::spinOnce();
        r.sleep();
    }
    std::cout << "ROS Shutdown" << std::endl;
    Q_EMIT rosShutdown();
}

// void QNode::mapID_Callback(const std_msgs::Int32::ConstPtr &msg)
// {
//     int mapID = msg->data;
//     Q_EMIT mapID_signal(mapID);
// }





int key = 0;
// double last=ros::Time::now().toSec();
// last=last*100;

 void QNode::kinectv2Image_Callback(const sensor_msgs::Image::ConstPtr &msg)
 {
     QImage::Format format;
     if(msg->encoding == "rgb8")
     {
         format = QImage::Format_RGB888;
         QImage kinectv2Image(&msg->data[0], msg->width, msg->height, format);
        //  Q_EMIT kinectv2Image_signal(kinectv2Image);   
         if (key == 0){
            key = 1;
            Q_EMIT kinectv2Image_signal(kinectv2Image);
            key = 0;
            ros::Duration(0.05).sleep();
            // printf("1\n");
         }
         
     }
 }

void QNode::amclPosition_Callback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr &msg)
{
    float amclPosition[2];
    amclPosition[0] = msg->pose.pose.position.x;
    amclPosition[1] = msg->pose.pose.position.y;
    if (key == 0){
        key = 1;
        Q_EMIT amclPosition_signal(amclPosition);
        ros::Duration(0.05).sleep();
        key = 0;
        // printf("x:%f,    y:%f\n",amclPosition[0],amclPosition[1]);
    }
}

void QNode::callingbell_Callback(const std_msgs::Int32::ConstPtr &msg)
{
    int Status = msg->data;
    Q_EMIT callingbell_signal(Status);
}

void QNode::agv_error_Callback(const std_msgs::Int32::ConstPtr &msg)
{
    int Status = msg->data;
    Q_EMIT agv_error_signal(Status);
}

void QNode::disappear_Callback(const std_msgs::Int32::ConstPtr &msg)
{
    int disappear_result = msg->data;
    Q_EMIT disappear_signal(disappear_result);
}

void QNode::abnormal_Callback(const std_msgs::Int32::ConstPtr &msg)
{
    int abnormal_result = msg->data;
    Q_EMIT abnormal_signal(abnormal_result);
}

void QNode::forward_control_pub()
{
    std_msgs::Int32 robot_motion;
    int rm = 1;
    robot_motion.data = rm;
    forward_pub.publish(robot_motion);
    ros::spinOnce();
}

void QNode::navigation_task_pub()
{
    std_msgs::Int32 navigation_task;
    int task = 4;
    navigation_task.data = task;
    navigation_pub.publish(navigation_task);
    ros::spinOnce();
}

void QNode::mode_switch_pub(bool switch_choice)
{
    std_msgs::Bool mode_switch;
    mode_switch.data = switch_choice;
    switch_pub.publish(mode_switch);
    ros::spinOnce();
}

}
