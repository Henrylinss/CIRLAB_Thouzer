#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "qsocket.hpp"
#include "qnode.hpp"
#include "ui_mainwindow.h"
#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QWidget>
#include <QCheckBox>
#include <qpushbutton.h>
#include <qlabel.h>
#include <QSizePolicy>
#include <qcombobox.h>
#include <qstring.h>
#include <QLineEdit>
#include <qdebug.h>
#include <QFrame>
#include <QGroupBox>
#include <qtreewidget.h>
#include <QRadioButton>
#include <QPainter>
#include <QMediaPlayer>
#include <QMediaPlaylist>
#include <QTimer>



namespace monitor {

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(int argc, char** argv, QWidget *parent = 0);
    ~MainWindow();
    
    int mapid;
    bool switch_choice;
    bool a_s;
    bool abnormal_walk_flag = false;
    bool abnormal_fall_flag = false;

    // Outside window (Left, Middle, Left)
    // Right Window
    QWidget *create_infor_window();
    // Middle Window
    QWidget *create_middle_window();
    // Left Window
    QWidget *create_left_window();
    QWidget *create_combine_window();
    //
    QWidget *create_control_window();

    // combine window -> infor_window
    QGroupBox *create_callingBell_Box();
    QGroupBox *create_disappear_Box();
    QGroupBox *create_AGV_err_Box();
    QGroupBox *create_abnormal_Box();

    QGroupBox *create_select_map_button();
    QGroupBox *create_follow_mode();
    // QGroupBox *create_remote_control();
    QGroupBox *create_self_move_api();
    QGroupBox *create_connect_Box();

    QWidget *create_connect_Infor();
    QWidget *create_connect_Infor_txt();

    QWidget *create_self_move_list();
    QWidget *create_self_move_list2();

    QWidget *create_alarm_callingBell();
    QWidget *create_alarm_disappear();
    QWidget *create_alarm_agv_err();
    QWidget *create_alarm_trace_err();
    QWidget *create_alarm_abnormal_walk();
    QWidget *create_alarm_abnormal_fall();
    void paintEvent(QPaintEvent *);

    public Q_SLOTS:
    // write you want slot function with qnode
    // --------------------------------------- //
    // void mapID_slot(int);
    void kinectv2Image_slot(QImage);
    void amclPosition_slot(float*);
    void callingbell_slot(int);
    void agv_error_slot(int);
    void disappear_slot(int);
    void abnormal_slot(int);
    void setLED(QLabel*, int, int);
    void playMp3();
    void stopMp3();
    // --------------------------------------- //

private:
    Ui::MainWindow ui;
    QNode qnode;
    int img_x;
    int img_y;
    int img_prex;
    int img_prey;
    int img_xstart = 1800; //1800
    int img_xend = 2800; //2800
    int img_ystart = 1670;//1670
    int img_yend = 2900; //2900
    int cellbell_count =0;
    int cellbell_count2 = 0;
    
    QString alarm_mp3 = "/home/cirlab/catkin_ws/src/qt_cirlab_monitor/image/alarm.mp3";

    QGroupBox *middle_window = new QGroupBox();
    QGroupBox *callingBell_Box = new QGroupBox(tr("Calling Bell"));
    QGroupBox *AGV_err_Box = new QGroupBox(tr("AGV_err"));
    QGroupBox *disappear_Box = new QGroupBox(tr("Disappear"));
    QGroupBox *abnormal_Box = new QGroupBox(tr("Abnormal Action"));
    

    QLabel *in_middle_window_show_map_label = new QLabel();
    QLabel *obstacles_detected_label = new QLabel();
    QLabel *image_label = new QLabel();

    QImage *obstacles_detected_image = new QImage();
    QImage *img_map = new QImage;
    QImage *abnormal_action_image_error = new QImage();
    QImage *abnormal_action_image_safe = new QImage();

    QLabel *alarm_infor_call = new QLabel(tr("Calling Bell"));
    QLabel *alarm_infor_disappear = new QLabel(tr("Disappear"));
    QLabel *alarm_infor_agvError = new QLabel(tr("AGV_err"));
    QLabel *alarm_infor_walk = new QLabel(tr("Walk"));
    QLabel *alarm_infor_fall = new QLabel(tr("Fall"));

    QLabel *callingBell_LED_A1 = new QLabel();
    QLabel *callingBell_LED_B1 = new QLabel();
    QLabel *disappear_LED_A1 = new QLabel();
    QLabel *disappear_LED_B1 = new QLabel();
    QLabel *agv_err_LED = new QLabel();
    QLabel *abnormal_LED_walk = new QLabel();
    QLabel *abnormal_LED_fall = new QLabel();
    QLabel *alarmC_LED_A1 = new QLabel(tr("A1"));
    QLabel *alarmC_LED_B1 = new QLabel(tr("B1"));
    QLabel *alarmD_LED_A1 = new QLabel(tr("A1"));
    QLabel *alarmD_LED_B1 = new QLabel(tr("B1"));

    QLineEdit *current_map_lineedit = new QLineEdit();

    QLabel *IP_label = new QLabel(tr("IP"));
    QLabel *PORT_label = new QLabel(tr("PORT"));
    QLabel *self_move_path_txt = new QLabel(tr("Path:"));


    QLineEdit *socket_IP = new QLineEdit();
    QLineEdit *socket_PORT = new QLineEdit();
    QLineEdit *self_move_path = new QLineEdit();


    QPushButton *close_window_button = new QPushButton("Quit");

    QPushButton *start_agv_follow_button = new QPushButton(tr("start_agv_follow"));
    QPushButton *end_agv_follow_button = new QPushButton(tr("end_agv_follow"));
    QPushButton *self_move_button = new QPushButton(tr("Self Move"));
    QPushButton *self_move_hold_button = new QPushButton(tr("self_move_hold"));
    QPushButton *self_move_resume_button = new QPushButton(tr("self_move_resume"));

//alarm information Button
    QPushButton *callingBell_reset_button = new QPushButton(tr("Reset"));
    QPushButton *disappear_reset_button = new QPushButton(tr("Reset"));
    QPushButton *agv_error_reset_button = new QPushButton(tr("Reset"));
    QPushButton *abnormal_walk_reset_button = new QPushButton(tr("Reset"));
    QPushButton *abnormal_fall_reset_button = new QPushButton(tr("Reset"));
// QMedia
    QMediaPlaylist *playlist;
    QMediaPlayer *mediaPlayer;

// QPushButton *remote_control_button = new QPushButton(tr("Remote Control"));

    QString filename = "/home/cirlab/catkin_ws/src/qt_cirlab_monitor/image/QT_map_4f.jpg";
    QString unpress_button_color = "background-color:rgb(233, 185, 110);"
                                   "border-radius:15px;"
                                   "border: 3px;"
                                   "border-color:rgb(233, 185, 110);"
                                   "font-size:13px";
    QString press_button_color = "background-color:#3BF169;"
                                 "border-radius:15px;"
                                 "border: 3px;"
                                 "border-color:#3BF169;"
                                 "font-size:13px";
    QString select_button = "font-size:26px";
    QString unpress_Title_button_color = "background-color:rgb(233, 185, 110);"
                           "border: 3px;"
                           "border-color:rgb(233, 185, 110);"
                           "font-size:15px";
    QString press_Title_button_color = "background-color:#3BF169;"
                           "border: 3px;"
                           "border-color:#3BF169;"
                           "font-size:15px";

private slots:
    // right window
    void close_window();

    // left window
    void start_agv_follow_button_clicked();
    void end_agv_follow_button_clicked();
    void self_move_button_clicked();
    void self_move_hold_button_clicked();
    void self_move_resume_button_clicked();
    void callingBell_reset_button_clicked();
    void disappear_reset_button_clicked();
    void agv_error_reset_button_clicked();
    void abnormal_fall_reset_button_clicked();
    void abnormal_walk_reset_button_clicked();
    
    // void playMp3();
    // void stopMp3();

};
}
#endif // MAINWINDOW_H
