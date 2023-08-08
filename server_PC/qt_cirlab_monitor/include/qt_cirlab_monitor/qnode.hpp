#ifndef QNODE_H
#define QNODE_H

#ifndef Q_MOC_RUN
#include <ros/ros.h>
#endif
#include <ros/network.h>
#include <std_msgs/Int16.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Float64.h>
#include <std_msgs/Float64MultiArray.h>
#include <std_msgs/Bool.h>
#include <sensor_msgs/Image.h>
#include <sensor_msgs/CompressedImage.h>
#include <geometry_msgs/Twist.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
//#include <qt_cirlab_monitor/cmd.h>
#include <string>
#include <QDebug>
#include <QImage>
#include <QLabel>
#include <QSettings>
#include <QStringListModel>
#include <QThread>
#include <QtConcurrent/QtConcurrent>

namespace monitor
{
class QNode : public QThread {
    Q_OBJECT

public:
    QNode(int argc, char** argv):init_argc(argc),init_argv(argv)
    {
        /*
            write pub/sub
            example : pub = n.advertise<std_msgs::Int32>("topic",100);
            example : sub = n.subscribe("topic",10000,&QNode::myCallback_img,this);
            sub = n.subscribe("/test", 1000, &QNode::mapid_Callback, this);
        */

        // mapID_sub = n.subscribe("/change_map", 1, &QNode::mapID_Callback, this);
        // actionRecognition_sub = n.subscribe("/action_recognition_results", 1, &QNode::actionRecognition_Callback, this);

        kinectv2Image_sub = n.subscribe("/kinectv2/image", 1, &QNode::kinectv2Image_Callback, this);
        amclPosition_sub = n.subscribe("/amcl_pose", 1, &QNode::amclPosition_Callback, this);
        callingbell_sub = n.subscribe("/socket/callingBell_status",1,&QNode::callingbell_Callback, this);
        abnormal_sub = n.subscribe("/abnormal_results",1,&QNode::abnormal_Callback, this);
        agv_error_sub = n.subscribe("/agv_status",1,&QNode::agv_error_Callback, this);
        disappear_sub = n.subscribe("/disappear_result",1,&QNode::disappear_Callback, this);

        forward_pub = n.advertise<std_msgs::Int32>("robot_motion", 1000);
        navigation_pub = n.advertise<std_msgs::Int32>("navigation_task", 1000);
        switch_pub = n.advertise<std_msgs::Bool>("mode_switch", 1000);
    }
    virtual ~QNode();

    int act;
    bool init();
    void run();

    
    /*
        write pub/sub function
        example: void myCallback_img(const sensor_msgs::CompressedImageConstPtr &msg);
    */

    // void mapID_Callback(const std_msgs::Int32::ConstPtr &msg);
    void kinectv2Image_Callback(const sensor_msgs::Image::ConstPtr &msg);
    void amclPosition_Callback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr &msg);
    void callingbell_Callback(const std_msgs::Int32::ConstPtr &msg);
    void agv_error_Callback(const std_msgs::Int32::ConstPtr &msg);
    void disappear_Callback(const std_msgs::Int32::ConstPtr &msg);
    void abnormal_Callback(const std_msgs::Int32::ConstPtr &msg);

    void forward_control_pub();

    void navigation_task_pub();
    void mode_switch_pub(bool switch_choice);

    enum LogLevel
    {
         Debug,
         Info,
         Warn,
         Error,
         Fatal
    };



Q_SIGNALS:

    /*
        if you want to subscribe data that signal event at mainwindow
        you need to write your signal event name in here.
    */

    void rosShutdown();
    // void mapID_signal(int);
    void kinectv2Image_signal(QImage);
    void amclPosition_signal(float*);
    void callingbell_signal(int);
    void agv_error_signal(int);
    void disappear_signal(int);
    void abnormal_signal(int);

private:
    int init_argc;
    char** init_argv;
    ros::NodeHandle n;

    /*
        write pub/sub name
        example: ros::Subscriber sub_name;
    */

    // ros::Subscriber mapID_sub;
    ros::Subscriber actionRecognition_sub;
    ros::Subscriber kinectv2Image_sub;
    ros::Subscriber amclPosition_sub;
    ros::Subscriber callingbell_sub;
    ros::Subscriber agv_error_sub;
    ros::Subscriber actionID_num_sub;
    ros::Subscriber disappear_sub;
    ros::Subscriber abnormal_sub;

    ros::Publisher forward_pub;

    ros::Publisher navigation_pub;
    ros::Publisher switch_pub;
};

}

#endif


