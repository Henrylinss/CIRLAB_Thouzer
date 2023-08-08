#include "../include/qt_cirlab_monitor/map.hpp"
#include "ui_map.h"


//  600, 450
map::map(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::map)
{
    ui->setupUi(this);
    this->setFixedSize(600, 450);
    QGridLayout *glayout = new QGridLayout(this);

    button_map1->setStyleSheet(init_button_color);
    button_map2->setStyleSheet(init_button_color);
    button_map3->setStyleSheet(init_button_color);
    button_map4->setStyleSheet(init_button_color);
    button_map5->setStyleSheet(init_button_color);

    glayout->addWidget(create_control(), 0, 0);
    glayout->addWidget(create_avoidance(), 1, 0);
    glayout->addWidget(create_navigation(), 0, 1);


    connect(button_map1, SIGNAL(clicked()), this, SLOT(button_map1_clicked()));
    connect(button_map2, SIGNAL(clicked()), this, SLOT(button_map2_clicked()));
    connect(button_map3, SIGNAL(clicked()), this, SLOT(button_map3_clicked()));
    connect(button_map4, SIGNAL(clicked()), this, SLOT(button_map4_clicked()));
    connect(button_map5, SIGNAL(clicked()), this, SLOT(button_map5_clicked()));
}

map::~map()
{
    delete ui;
}

QGroupBox *map::create_avoidance()
{
    QGroupBox *avoidance_window = new QGroupBox(tr("Avoidance Obstacle"));
    avoidance_window->setFixedSize(300, 150);

    QWidget *no_avoidance = new QWidget();
    QWidget *avoidance = new QWidget();
    QVBoxLayout *vlayout = new QVBoxLayout();
    QHBoxLayout *hlayout1 = new QHBoxLayout();
    QHBoxLayout *hlayout2 = new QHBoxLayout();
    QImage *image1 = new QImage();
    QImage *image2 = new QImage();
    QLabel *label1 = new QLabel();
    QLabel *label2 = new QLabel();
    QLabel *label3 = new QLabel(tr("Obstacles detected"));
    QLabel *label4 = new QLabel(tr("No obstacles detected"));

    image1->load("/home/thouzer/catkin_ws/src/qt_cirlab_monitor/image/status_normal.png");
    image2->load("/home/thouzer/catkin_ws/src/qt_cirlab_monitor/image/status_error.png");
    label1->setPixmap(QPixmap::fromImage(*image1));
    label2->setPixmap(QPixmap::fromImage(*image2));

    avoidance->setLayout(hlayout1);
    no_avoidance->setLayout(hlayout2);

    hlayout1->addWidget(label1);
    hlayout1->addWidget(label3);
    hlayout2->addWidget(label2);
    hlayout2->addWidget(label4);

    vlayout->addWidget(avoidance);
    vlayout->addWidget(no_avoidance);
    vlayout->addStretch(1);
    avoidance_window->setLayout(vlayout);

    return avoidance_window;
}

QGroupBox *map::create_navigation()
{
    QGroupBox *navigation_window = new QGroupBox(tr("Navigation"));
    navigation_window->setFixedSize(300, 300);
    QWidget *current_map_text = new QWidget();
    QVBoxLayout *vlayout = new QVBoxLayout();
    QHBoxLayout *hlayout = new QHBoxLayout();
    QRadioButton *radio1 = new QRadioButton(tr("Navigation to 1F"));
    QRadioButton *radio2 = new QRadioButton(tr("Navigation to 2F"));
    QRadioButton *radio3 = new QRadioButton(tr("Navigation to 3F"));
    QRadioButton *radio4 = new QRadioButton(tr("Navigation to 4F"));
    QRadioButton *radio5 = new QRadioButton(tr("Navigation to 5F"));
    current_map_text->setLayout(hlayout);

    hlayout->addWidget(current_map_label, 0);
    hlayout->addWidget(current_map_lineedit, 1);

    vlayout->addWidget(current_map_text);
    vlayout->addWidget(radio1);
    vlayout->addWidget(radio2);
    vlayout->addWidget(radio3);
    vlayout->addWidget(radio4);
    vlayout->addWidget(radio5);

    vlayout->addStretch(1);
    navigation_window->setLayout(vlayout);

    return navigation_window;
}

QGroupBox *map::create_control()
{
    QGroupBox *control_window = new QGroupBox(tr("Base Control"));
    QGridLayout *glayout = new QGridLayout();
    control_window->setFixedSize(300, 300);
    glayout->addWidget(button_map1, 0, 1);
    glayout->addWidget(button_map2, 1, 0);
    glayout->addWidget(button_map3, 1, 1);
    glayout->addWidget(button_map4, 1, 2);
    glayout->addWidget(button_map5, 2, 1);

    control_window->setLayout(glayout);

    return control_window;
}


void map::button_map1_clicked()
{
    button_map1->setStyleSheet(press_button_color);
    button_map2->setStyleSheet(unpress_button_color);
    button_map3->setStyleSheet(unpress_button_color);
    button_map4->setStyleSheet(unpress_button_color);
    button_map5->setStyleSheet(unpress_button_color);
}

void map::button_map2_clicked()
{
    button_map1->setStyleSheet(unpress_button_color);
    button_map2->setStyleSheet(press_button_color);
    button_map3->setStyleSheet(unpress_button_color);
    button_map4->setStyleSheet(unpress_button_color);
    button_map5->setStyleSheet(unpress_button_color);
}

void map::button_map3_clicked()
{
    button_map1->setStyleSheet(unpress_button_color);
    button_map2->setStyleSheet(unpress_button_color);
    button_map3->setStyleSheet(press_button_color);
    button_map4->setStyleSheet(unpress_button_color);
    button_map5->setStyleSheet(unpress_button_color);
}

void map::button_map4_clicked()
{
    button_map1->setStyleSheet(unpress_button_color);
    button_map2->setStyleSheet(unpress_button_color);
    button_map3->setStyleSheet(unpress_button_color);
    button_map4->setStyleSheet(press_button_color);
    button_map5->setStyleSheet(unpress_button_color);
}

void map::button_map5_clicked()
{
    button_map1->setStyleSheet(unpress_button_color);
    button_map2->setStyleSheet(unpress_button_color);
    button_map3->setStyleSheet(unpress_button_color);
    button_map4->setStyleSheet(unpress_button_color);
    button_map5->setStyleSheet(press_button_color);
}
