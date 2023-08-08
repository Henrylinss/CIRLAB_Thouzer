#include "../include/qt_cirlab_monitor/mainwindow.hpp"
#include "ui_mainwindow.h"
#include <iostream>

namespace monitor {

using namespace Qt;

MainWindow::MainWindow(int argc, char** argv, QWidget *parent) :
    QMainWindow(parent), qnode(argc, argv)
{
    qnode.init();
    ui.setupUi(this);
    this->setWindowTitle("cirlab-monitor");
    this->setFixedSize(1500, 740);//1480 700
    QHBoxLayout *hlayout = new QHBoxLayout();

    ui.centralWidget->setLayout(hlayout);
    ui.centralWidget->setFixedSize(1480, 720);//1480 660

    hlayout->addWidget(create_left_window());
    hlayout->addWidget(create_middle_window());

    connect(close_window_button, SIGNAL(clicked()), this, SLOT(close_window()));

    connect(start_agv_follow_button, SIGNAL(clicked()), this, SLOT(start_agv_follow_button_clicked()));
    connect(end_agv_follow_button, SIGNAL(clicked()), this, SLOT(end_agv_follow_button_clicked()));
    connect(self_move_button, SIGNAL(clicked()), this, SLOT(self_move_button_clicked()));
    connect(self_move_hold_button, SIGNAL(clicked()), this, SLOT(self_move_hold_button_clicked()));
    connect(self_move_resume_button, SIGNAL(clicked()), this, SLOT(self_move_resume_button_clicked()));
    connect(callingBell_reset_button, SIGNAL(clicked()), this, SLOT(callingBell_reset_button_clicked()));
    connect(disappear_reset_button, SIGNAL(clicked()), this, SLOT(disappear_reset_button_clicked()));
    connect(agv_error_reset_button, SIGNAL(clicked()), this, SLOT(agv_error_reset_button_clicked()));
    connect(abnormal_fall_reset_button, SIGNAL(clicked()), this, SLOT(abnormal_fall_reset_button_clicked()));
    connect(abnormal_walk_reset_button, SIGNAL(clicked()), this, SLOT(abnormal_walk_reset_button_clicked()));
    

    connect(&qnode, SIGNAL(callingbell_signal(int)), this, SLOT(callingbell_slot(int)));
    connect(&qnode, SIGNAL(agv_error_signal(int)), this, SLOT(agv_error_slot(int)));
    connect(&qnode, SIGNAL(disappear_signal(int)), this, SLOT(disappear_slot(int)));
    connect(&qnode, SIGNAL(abnormal_signal(int)), this, SLOT(abnormal_slot(int)));
    connect(&qnode, SIGNAL(rosShutdown()), this, SLOT(close()));

    connect(&qnode, SIGNAL(kinectv2Image_signal(QImage)), this, SLOT(kinectv2Image_slot(QImage)));
    connect(&qnode, SIGNAL(amclPosition_signal(float*)), this, SLOT(amclPosition_slot(float*)));
    playlist = new QMediaPlaylist;
    mediaPlayer = new QMediaPlayer;
    playlist->addMedia(QUrl::fromLocalFile(alarm_mp3));
    mediaPlayer->setPlaylist(playlist);
}

MainWindow::~MainWindow(){
    delete mediaPlayer;
    delete playlist;
}

// Right Window
QWidget *MainWindow::create_infor_window()
{
    QWidget *right_window = new QWidget();
    QVBoxLayout *vlayout = new QVBoxLayout();

    right_window->setLayout(vlayout);

    vlayout->addWidget(create_callingBell_Box());
    vlayout->addWidget(create_disappear_Box());
    vlayout->addWidget(create_abnormal_Box());
    vlayout->addWidget(create_AGV_err_Box());
    vlayout->addWidget(create_connect_Box());
    
//    vlayout->addWidget(close_window_button);

    return right_window;
}

int led_size = 6;

QGroupBox *MainWindow::create_callingBell_Box()
{
    QHBoxLayout *hlayout = new QHBoxLayout();

    callingBell_Box->setLayout(hlayout);
    callingBell_reset_button->setFixedSize(100, 20);//120,25
    setLED(callingBell_LED_A1,0,led_size);
    setLED(callingBell_LED_B1,0,led_size);
    hlayout->addWidget(alarmC_LED_A1);
    hlayout->addWidget(callingBell_LED_A1);
    hlayout->addWidget(alarmC_LED_B1);
    hlayout->addWidget(callingBell_LED_B1);
    hlayout->addWidget(callingBell_reset_button);
    return callingBell_Box;
}

QGroupBox *MainWindow::create_disappear_Box()
{
    QHBoxLayout *hlayout = new QHBoxLayout();

    disappear_Box->setLayout(hlayout);
    disappear_reset_button->setFixedSize(100, 20);//120,25
    setLED(disappear_LED_A1,0,led_size);
    setLED(disappear_LED_B1,0,led_size);
    hlayout->addWidget(alarmD_LED_A1);
    hlayout->addWidget(disappear_LED_A1);
    hlayout->addWidget(alarmD_LED_B1);
    hlayout->addWidget(disappear_LED_B1);
    hlayout->addWidget(disappear_reset_button);
    return disappear_Box;
}

QGroupBox *MainWindow::create_AGV_err_Box()
{
    
    QHBoxLayout *hlayout = new QHBoxLayout();

    AGV_err_Box->setLayout(hlayout);
    setLED(agv_err_LED,0,led_size);
    agv_error_reset_button->setFixedSize(100, 20);//120,25
    hlayout->addWidget(agv_err_LED);
    hlayout->addSpacing(35); 
    hlayout->addWidget(agv_error_reset_button);
    return AGV_err_Box;
}

QGroupBox *MainWindow::create_abnormal_Box()
{
    
    QVBoxLayout *vlayout = new QVBoxLayout();

    abnormal_Box->setLayout(vlayout);

    vlayout->addWidget(create_alarm_abnormal_walk());
    vlayout->addWidget(create_alarm_abnormal_fall());
    return abnormal_Box;
}

// Middle Window
QWidget *MainWindow::create_middle_window()
{
    QHBoxLayout *hlayout = new QHBoxLayout();

    middle_window->setFixedSize(610, 600);
    middle_window->setLayout(hlayout);

    in_middle_window_show_map_label->setFixedSize(500, 500);

    hlayout->addWidget(in_middle_window_show_map_label);

    return middle_window;
}


// Left Window
QWidget *MainWindow::create_left_window()
{
    QWidget *left_window = new QWidget();
    QVBoxLayout *vlayout = new QVBoxLayout();

    left_window->setFixedSize(660, 700);//620 660
    left_window->setLayout(vlayout);

    image_label->setAlignment(Qt::AlignCenter | Qt::AlignHCenter);

    vlayout->addWidget(image_label);
    vlayout->addWidget(create_combine_window());

    return left_window;
}
QWidget *MainWindow::create_control_window()
{
    QWidget *control_window = new QWidget();
    QVBoxLayout *vlayout = new QVBoxLayout();

    control_window->setLayout(vlayout);

    vlayout->addWidget(create_follow_mode());
    vlayout->addWidget(create_self_move_api());
    // vlayout->addWidget(create_remote_control());

    return control_window;
}
QWidget *MainWindow::create_combine_window()
{
    QWidget *combine_window = new QWidget();
    QHBoxLayout *glayout = new QHBoxLayout();

    int h = 30;
    int w = 115;//100

    combine_window->setFixedSize(640, 520);//600 460
    combine_window->setLayout(glayout);



    start_agv_follow_button->setStyleSheet(unpress_button_color);
    end_agv_follow_button->setStyleSheet(unpress_button_color);
    self_move_button->setStyleSheet(unpress_button_color);
    self_move_hold_button->setStyleSheet(unpress_button_color);
    self_move_resume_button->setStyleSheet(unpress_button_color);

    start_agv_follow_button->setFixedSize(w, h);
    end_agv_follow_button->setFixedSize(w, h);
    self_move_button->setFixedSize(w, h);
    self_move_hold_button->setFixedSize(w, h);
    self_move_resume_button->setFixedSize(w, h);

    alarm_infor_call->setStyleSheet("QLabel {color : balck}");
    alarm_infor_disappear->setStyleSheet("QLabel {color : black}");
    alarm_infor_agvError->setStyleSheet("QLabel {color : black}");
    alarm_infor_walk->setStyleSheet("QLabel {color : black}");
    alarm_infor_fall->setStyleSheet("QLabel {color : black}");

    glayout->addWidget(create_infor_window());
    glayout->addWidget(create_control_window());


    return combine_window;
}



QGroupBox *MainWindow::create_follow_mode()
{
    QGroupBox *follow_api = new QGroupBox(tr("Follow-me"));
    QHBoxLayout *glayout = new QHBoxLayout();

    follow_api->setFixedSize(365,75);
    follow_api->setLayout(glayout);

    glayout->addWidget(start_agv_follow_button);
    glayout->addWidget(end_agv_follow_button);

    return follow_api;
}

QGroupBox *MainWindow::create_self_move_api()
{
    QGroupBox *self_move_api = new QGroupBox(tr("Memory Trace Mode"));
    QGridLayout *glayout = new QGridLayout();
    self_move_api->setFixedSize(365,180);
    self_move_api->setLayout(glayout);

    glayout->addWidget(create_self_move_list(),0,0);
    glayout->addWidget(create_self_move_list2(),1,0);

    return self_move_api;
}

// QGroupBox *MainWindow::create_remote_control()
// {
//     QGroupBox *remote_control = new QGroupBox(tr("Remote Control"));
//     QVBoxLayout *vlayout = new QVBoxLayout();
// //    moving_direction_window->setFixedSize(330, 80);
//     remote_control->setLayout(vlayout);
//     return remote_control;
// }


QWidget *MainWindow::create_connect_Infor()
{
    QWidget *connect_Infor = new QWidget();
    QVBoxLayout *glayout = new QVBoxLayout();

    connect_Infor->setLayout(glayout);

    glayout->addWidget(socket_IP);
    glayout->addWidget(socket_PORT);

    return connect_Infor;
}

QWidget *MainWindow::create_connect_Infor_txt()
{
    QWidget *connect_Infor_txt = new QWidget();
    QVBoxLayout *glayout = new QVBoxLayout();

    connect_Infor_txt->setLayout(glayout);

    glayout->addWidget(IP_label);
    glayout->addWidget(PORT_label);

    return connect_Infor_txt;
}

QGroupBox *MainWindow::create_connect_Box()
{
    QGroupBox *connect_Box = new QGroupBox(tr("AGV's IP and PORT"));
    QHBoxLayout *hlayout = new QHBoxLayout();

    connect_Box->setFixedSize(215, 100);
    connect_Box->setLayout(hlayout);

    hlayout->addWidget(create_connect_Infor_txt());
    hlayout->addWidget(create_connect_Infor());

    return connect_Box;
}

QWidget *MainWindow::create_self_move_list()
{
    QWidget *create_self_move_list = new QWidget();
    QHBoxLayout *hlayout = new QHBoxLayout();

    create_self_move_list->setLayout(hlayout);
    self_move_path_txt->setFixedSize(45,25);

    hlayout->addWidget(self_move_path_txt);
    hlayout->addWidget(self_move_path);

    hlayout->addWidget(self_move_button);
    return create_self_move_list;
}

QWidget *MainWindow::create_self_move_list2()
{
    QWidget *create_self_move_list2 = new QWidget();
    QHBoxLayout *hlayout = new QHBoxLayout();

    create_self_move_list2->setLayout(hlayout);

    hlayout->addWidget(self_move_hold_button);
    hlayout->addWidget(self_move_resume_button);

    return create_self_move_list2;
}

// create alarm Box

QWidget *MainWindow::create_alarm_callingBell()
{
    QWidget *create_alarm_callingBell = new QWidget();
    QHBoxLayout *hlayout = new QHBoxLayout();

    create_alarm_callingBell->setLayout(hlayout);
    callingBell_reset_button->setFixedSize(150, 25);
    setLED(callingBell_LED_A1,0,led_size);
    setLED(callingBell_LED_B1,0,led_size);
    hlayout->addWidget(alarm_infor_call);
    hlayout->addWidget(alarmC_LED_A1);
    hlayout->addWidget(callingBell_LED_A1);
    hlayout->addWidget(alarmC_LED_B1);
    hlayout->addWidget(callingBell_LED_B1);
    hlayout->addWidget(callingBell_reset_button);
    return create_alarm_callingBell;
}

QWidget *MainWindow::create_alarm_disappear()
{
    QWidget *create_alarm_disappear = new QWidget();
    QHBoxLayout *hlayout = new QHBoxLayout();

    create_alarm_disappear->setLayout(hlayout);
    disappear_reset_button->setFixedSize(150, 25);

    setLED(disappear_LED_A1,0,led_size);
    setLED(disappear_LED_B1,0,led_size);
    hlayout->addWidget(alarm_infor_disappear);
    hlayout->addWidget(alarmD_LED_A1);
    hlayout->addWidget(disappear_LED_A1);
    hlayout->addWidget(alarmD_LED_B1);
    hlayout->addWidget(disappear_LED_B1);
    hlayout->addWidget(disappear_reset_button);
    return create_alarm_disappear;
}

QWidget *MainWindow::create_alarm_agv_err()
{
    QWidget *create_alarm_agv_err = new QWidget();
    QHBoxLayout *hlayout = new QHBoxLayout();

    create_alarm_agv_err->setLayout(hlayout);

    setLED(agv_err_LED,0,led_size);
    hlayout->addWidget(alarm_infor_agvError);
    hlayout->addWidget(agv_err_LED);
    hlayout->addWidget(agv_error_reset_button);
    return create_alarm_agv_err;
}

QWidget *MainWindow::create_alarm_abnormal_walk()
{
    QWidget *alarm_abnormal_walk = new QWidget();
    QHBoxLayout *hlayout = new QHBoxLayout();

    alarm_abnormal_walk->setLayout(hlayout);
    abnormal_walk_reset_button->setFixedSize(100, 20);
    setLED(abnormal_LED_walk,0,led_size);
    hlayout->addWidget(alarm_infor_walk);
    hlayout->addWidget(abnormal_LED_walk);
    hlayout->addWidget(abnormal_walk_reset_button);
    return alarm_abnormal_walk;
}

QWidget *MainWindow::create_alarm_abnormal_fall()
{
    QWidget *alarm_abnormal_fall = new QWidget();
    QHBoxLayout *hlayout = new QHBoxLayout();

    alarm_abnormal_fall->setLayout(hlayout);
    abnormal_fall_reset_button->setFixedSize(100, 20);
    setLED(abnormal_LED_fall,0,led_size);
    hlayout->addWidget(alarm_infor_fall);
    hlayout->addWidget(abnormal_LED_fall);
    hlayout->addWidget(abnormal_fall_reset_button);
    return alarm_abnormal_fall;
}

// create_right_window() SLOT Function
void MainWindow::close_window()
{
    close();
}

void MainWindow::paintEvent(QPaintEvent *)
{
    img_map->load(filename);
    *img_map=img_map->copy(img_xstart, img_ystart, img_xend-img_xstart, img_yend-img_ystart);
    *img_map=img_map->scaled(in_middle_window_show_map_label->width(), in_middle_window_show_map_label->height(), Qt::IgnoreAspectRatio);//Qt::IgnoreAspectRatio  KeepAspectRatio
    QPainter painter(img_map);
    QPen pen;
    
    pen.setColor(204);
    pen.setWidth(7);
    pen.setCapStyle(Qt::MPenCapStyle);
    pen.setStyle(Qt::DashDotDotLine);
    painter.setPen(pen);

    painter.drawPoint(img_x, img_y);
    //img_x, img_y
    in_middle_window_show_map_label->setPixmap(QPixmap::fromImage(*img_map));
    in_middle_window_show_map_label->setAlignment(Qt::AlignCenter);
}

// create_left_window() SLOT Function
void MainWindow::kinectv2Image_slot(QImage kinectv2Image)
{
    image_label->setPixmap(QPixmap::fromImage(kinectv2Image));
    image_label->show();
}
void MainWindow::callingbell_slot(int bell_Status)
{
    if(bell_Status == 0)
    {
        cellbell_count++;
    }
    else if (bell_Status == 1)
    {
        cellbell_count2++;
    }


    if(cellbell_count%2==0)
    {
        setLED(callingBell_LED_A1,0,led_size);
    }
    else
    {
        setLED(callingBell_LED_A1,1,led_size);
    }

    if(cellbell_count2%2==0)
    {
        setLED(callingBell_LED_B1,0,led_size);
    }
    else
    {
        setLED(callingBell_LED_B1,1,led_size);
    }


    callingBell_Box->update();
}

void MainWindow::agv_error_slot(int agv_Status)
{

    if(agv_Status==1)
    {
        setLED(agv_err_LED,1,led_size);
    }

    else
    {
        setLED(agv_err_LED,0,led_size);
    }
    AGV_err_Box->update();
}

void MainWindow::disappear_slot(int disappear_result)
{

    if(disappear_result==0)
    {
        // setLED(disappear_LED_A1,0,led_size);
        setLED(disappear_LED_A1,0,led_size);
    }

    else if (disappear_result==1)
    {
        setLED(disappear_LED_A1,1,led_size);
        playMp3();
    }
    disappear_Box->update();
}

void MainWindow::abnormal_slot(int abnormal_result)
{
    if(abnormal_result==0)
    {
        setLED(abnormal_LED_fall,0,led_size);//LED
        setLED(abnormal_LED_walk,0,led_size);
        stopMp3();//MP3
        abnormal_fall_flag = false;
        abnormal_walk_flag = false;

    }
    // fall
    else if (abnormal_result==1) 
    {
        setLED(abnormal_LED_fall,1,led_size);
        setLED(abnormal_LED_walk,0,led_size);
        if (abnormal_fall_flag == false){
            abnormal_fall_flag = true;
            playMp3();
        }
    }
    //walk
    else if (abnormal_result==2)
    {
        setLED(abnormal_LED_walk,1,led_size);
        setLED(abnormal_LED_fall,0,led_size);
        if (abnormal_walk_flag == false){
            abnormal_walk_flag = true;
            playMp3();
        }
    }
    abnormal_Box->update();
}

void MainWindow::amclPosition_slot(float* amclPosition)
{
    // printf("x1:%f,    y1:%f\n",amclPosition[0],amclPosition[1]);
    int img_x_multi, img_y_multi;
    float img_x_plus, img_y_plus;

    img_x_plus = amclPosition[0] + 100;
    img_y_plus = amclPosition[1] - 100;

    img_x_plus = img_x_plus * 20;
    img_y_plus = img_y_plus * 20;

    img_x_plus = img_x_plus - img_xstart;
    img_y_plus = img_y_plus - img_ystart;

    // printf("inputimg_x:%f,    inputimg_y:%f\n",amclPosition[0],amclPosition[1]);
    img_prex = int((fabs(amclPosition[0]+100.0)*20.0 - float(img_xstart))*(float(in_middle_window_show_map_label->width())/float((img_xend-img_xstart))));
    img_prey = int((fabs(amclPosition[1]-100.0)*20.0 - float(img_ystart))*(float(in_middle_window_show_map_label->height())/float((img_yend-img_ystart))));
    // printf("img_x:%d,    img_y:%d\n",img_prex,img_prey);
    // printf("img_x1:%d,    img_y1:%d\n",img_x,img_y);
    //  if ((img_prex>160) && (img_prey < 400))
    //  {
    //     img_x=img_prex;
    //     img_y=img_prey;
    //  }
    if ((int(amclPosition[0])!=0) && (int(amclPosition[1]) != 0))
    {
    img_x=img_prex;
    img_y=img_prey;
    }
    middle_window->update();
}



// create_control() SLOT Function
void MainWindow::start_agv_follow_button_clicked()
{
    QString str = socket_IP->text();
    QByteArray byteArray=str.toLocal8Bit ();
    char* ip=byteArray.data();
    int PORT = socket_PORT->text().toInt();
    Send qsocket;
    start_agv_follow_button->setStyleSheet(press_button_color);
    end_agv_follow_button->setStyleSheet(unpress_button_color);
    self_move_button->setStyleSheet(unpress_button_color);
    self_move_hold_button->setStyleSheet(unpress_button_color);
    self_move_resume_button->setStyleSheet(unpress_button_color);
    qsocket.Do("start_agv_follow", ip, PORT);

}

void MainWindow::end_agv_follow_button_clicked()
{
    QString str = socket_IP->text();
    QByteArray byteArray=str.toLocal8Bit ();
    char* ip=byteArray.data();
    int PORT = socket_PORT->text().toInt();
    Send qsocket;
    start_agv_follow_button->setStyleSheet(unpress_button_color);
    end_agv_follow_button->setStyleSheet(press_button_color);
    self_move_button->setStyleSheet(unpress_button_color);
    self_move_hold_button->setStyleSheet(unpress_button_color);
    self_move_resume_button->setStyleSheet(unpress_button_color);
    qsocket.Do("end_agv_follow", ip, PORT);

}

void MainWindow::self_move_button_clicked()
{
    QString str = socket_IP->text();
    std::string move_path = self_move_path->text().toStdString();
    std::string api = "self_move_";
    std::string add = api+move_path;
    char* path = new char[add.length()+1];
    strcpy(path,add.c_str());
    QByteArray byteArray=str.toLocal8Bit ();
    char* ip=byteArray.data();
    int PORT = socket_PORT->text().toInt();
    Send qsocket;
    start_agv_follow_button->setStyleSheet(unpress_button_color);
    end_agv_follow_button->setStyleSheet(unpress_button_color);
    self_move_button->setStyleSheet(press_button_color);
    self_move_hold_button->setStyleSheet(unpress_button_color);
    self_move_resume_button->setStyleSheet(unpress_button_color);
    qsocket.Do(path, ip, PORT);
    delete [] path;
}

void MainWindow::self_move_hold_button_clicked()
{
    QString str = socket_IP->text();
    QByteArray byteArray=str.toLocal8Bit ();
    char* ip=byteArray.data();
    int PORT = socket_PORT->text().toInt();
    Send qsocket;
    start_agv_follow_button->setStyleSheet(unpress_button_color);
    end_agv_follow_button->setStyleSheet(unpress_button_color);
    self_move_button->setStyleSheet(unpress_button_color);
    self_move_hold_button->setStyleSheet(press_button_color);
    self_move_resume_button->setStyleSheet(unpress_button_color);
    qsocket.Do("self_move_hold", ip, PORT);
}

void MainWindow::self_move_resume_button_clicked()
{
    QString str = socket_IP->text();
    QByteArray byteArray=str.toLocal8Bit ();
    char* ip=byteArray.data();
    int PORT = socket_PORT->text().toInt();
    Send qsocket;
    start_agv_follow_button->setStyleSheet(unpress_button_color);
    end_agv_follow_button->setStyleSheet(unpress_button_color);
    self_move_button->setStyleSheet(unpress_button_color);
    self_move_hold_button->setStyleSheet(unpress_button_color);
    self_move_resume_button->setStyleSheet(press_button_color);
    qsocket.Do("self_move_resume", ip, PORT);

}

void MainWindow::callingBell_reset_button_clicked()
{
    setLED(callingBell_LED_A1,0,led_size);
    setLED(callingBell_LED_B1,0,led_size);
    cellbell_count = 0;
    cellbell_count2 = 0;
}

void MainWindow::disappear_reset_button_clicked()
{
    setLED(disappear_LED_A1,0,led_size);
    setLED(disappear_LED_B1,0,led_size);
    // playMp3();
}

void MainWindow::agv_error_reset_button_clicked()
{
    QString str = socket_IP->text();
    QByteArray byteArray=str.toLocal8Bit ();
    char* ip=byteArray.data();
    int PORT = socket_PORT->text().toInt();
    Send qsocket;
    qsocket.Do("AGV_debug", ip, PORT);
    setLED(agv_err_LED,0,led_size);
}

void MainWindow::abnormal_fall_reset_button_clicked()
{
    // socket client
    QString str = socket_IP->text();
    QByteArray byteArray=str.toLocal8Bit ();
    char* ip=byteArray.data();
    int PORT = socket_PORT->text().toInt();
    Send qsocket;
    qsocket.Do("self_move_resume", ip, PORT);
    // LED and stopMp3
    setLED(abnormal_LED_fall,0,led_size);
    stopMp3();
}

void MainWindow::abnormal_walk_reset_button_clicked()
{
    // socket client
    QString str = socket_IP->text();
    QByteArray byteArray=str.toLocal8Bit ();
    char* ip=byteArray.data();
    int PORT = socket_PORT->text().toInt();
    Send qsocket;
    qsocket.Do("self_move_resume", ip, PORT);
    // LED and stopMp3
    setLED(abnormal_LED_walk,0,led_size);
    stopMp3();
}

void MainWindow::playMp3()
{
    playlist->setPlaybackMode(QMediaPlaylist::Loop);
    mediaPlayer->play();
}

void MainWindow::stopMp3()
{
    mediaPlayer->stop();
    playlist->setPlaybackMode(QMediaPlaylist::CurrentItemOnce);
}

// function of setting LED, change color
void MainWindow::setLED(QLabel* label, int color, int size)
{

    label->setText("");

    QString min_width = QString("min-width: %1px;").arg(size);              // mini W：size
    QString min_height = QString("min-height: %1px;").arg(size);            // mini H：size
    QString max_width = QString("max-width: %1px;").arg(size);              // mini W：size
    QString max_height = QString("max-height: %1px;").arg(size);            // mini H：size

    QString border_radius = QString("border-radius: %1px;").arg(size/2);
    QString border = QString("border:1px solid black;");
    // set background color
    QString background = "background-color:";
    switch (color) {
    case 0:
        // gray
        background += "rgb(190,190,190)";
        break;
    case 1:
        // red
        background += "rgb(255,0,0)";
        break;
    case 2:
        // green
        background += "rgb(0,255,0)";
        break;
    case 3:
        // yellow
        background += "rgb(255,255,0)";
        break;
    case 4:
        //blue
        background += "rgb(135,206,250)";
        break;
    default:
        break;
    }

    const QString SheetStyle = min_width + min_height + max_width + max_height + border_radius + border + background;
    label->setStyleSheet(SheetStyle);
}

}
