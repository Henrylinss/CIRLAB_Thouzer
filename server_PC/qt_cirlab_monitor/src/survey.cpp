#include "../include/qt_cirlab_monitor/survey.hpp"
#include "ui_survey.h"

survey::survey(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::survey)
{
    ui->setupUi(this);
    this->setFixedSize(600, 300);
    QHBoxLayout *hlayout = new QHBoxLayout(this);
    if (qrviz == NULL) {
            qrviz = new QRviz();
    }
    QTreeWidget *treeWidget = new QTreeWidget();

    // GLobal Options
    QTreeWidgetItem* Global = new QTreeWidgetItem(QStringList() << "Global Options");
    Global->setIcon(0, QIcon(QString("/home/thouzer/catkin_ws/src/qt_cirlab_monitor/image/options.png")));
    treeWidget->setHeaderLabels(QStringList()<<"key" <<"value");
    treeWidget->addTopLevelItem(Global);
    Global->setExpanded(true);

    // FixFrame
    QTreeWidgetItem* Fixed_frame =new QTreeWidgetItem(QStringList() << "Fixed Frame");
    fixed_box = new QComboBox();
    fixed_box->addItem("/map");
    fixed_box->setMaximumWidth(150);
    fixed_box->setEditable(true);
    Global->addChild(Fixed_frame);
    treeWidget->setItemWidget(Fixed_frame, 1, fixed_box);

    // Grid
    QTreeWidgetItem* Grid = new QTreeWidgetItem(QStringList() << "Grid");
    Grid->setIcon(0, QIcon(QString("/home/thouzer/catkin_ws/src/qt_cirlab_monitor/image/Grid.png")));
    Grid_Check = new QCheckBox();
    treeWidget->addTopLevelItem(Grid);
    treeWidget->setItemWidget(Grid, 1, Grid_Check);
    Grid->setExpanded(true);
    QTreeWidgetItem* Grid_Color = new QTreeWidgetItem(QStringList() << "Color");
    Grid->addChild(Grid_Color);
    Grid_Color_Box = new QComboBox();
    Grid_Color_Box->addItem("160;160;160");
    Grid_Color_Box->setEditable(true);
    Grid_Color_Box->setMaximumWidth(150);
    treeWidget->setItemWidget(Grid_Color, 1, Grid_Color_Box);

    // Map
    QTreeWidgetItem* Map = new QTreeWidgetItem(QStringList() << "Map");
    Map->setIcon(0, QIcon(QString("/home/thouzer/catkin_ws/src/qt_cirlab_monitor/image/Map.png")));
    Map_Check = new QCheckBox();
    treeWidget->addTopLevelItem(Map);
    treeWidget->setItemWidget(Map, 1, Map_Check);
    QTreeWidgetItem* MapTopic = new QTreeWidgetItem(QStringList() << "Topic");
    Map_Topic_box = new QComboBox();
    Map_Topic_box->addItem("/map");
    Map_Topic_box->setEditable(true);
    Map_Topic_box->setMaximumWidth(150);
    Map->addChild(MapTopic);
    treeWidget->setItemWidget(MapTopic, 1, Map_Topic_box);

    // LaserScan
    QTreeWidgetItem* LaserScan = new QTreeWidgetItem(QStringList() << "LaserScan");
    LaserScan->setIcon(0, QIcon(QString("/home/thouzer/catkin_ws/src/qt_cirlab_monitor/image/LaserScan.png")));
    Laser_Check = new QCheckBox();
    treeWidget->addTopLevelItem(LaserScan);
    treeWidget->setItemWidget(LaserScan, 1, Laser_Check);
    QTreeWidgetItem* LaserTopic = new QTreeWidgetItem(QStringList() << "Topic");
    Laser_Topic_box = new QComboBox();
    Laser_Topic_box->addItem("/scan");
    Laser_Topic_box->setEditable(true);
    Laser_Topic_box->setMaximumWidth(150);
    LaserScan->addChild(LaserTopic);
    treeWidget->setItemWidget(LaserTopic, 1, Laser_Topic_box);

    // PoseArray
    QTreeWidgetItem* PoseArray = new QTreeWidgetItem(QStringList() << "PoseArray");
    PoseArray->setIcon(0, QIcon(QString("/home/thouzer/catkin_ws/src/qt_cirlab_monitor/image/PoseArray.png")));
    PoseArray_Check = new QCheckBox();
    treeWidget->addTopLevelItem(PoseArray);
    treeWidget->setItemWidget(PoseArray, 1, PoseArray_Check);
    QTreeWidgetItem* PoseArrayTopic = new QTreeWidgetItem(QStringList() << "Topic");
    PoseArray_Topic_box = new QComboBox();
    PoseArray_Topic_box->addItem("/particlecloud");
    PoseArray_Topic_box->setEditable(true);
    PoseArray_Topic_box->setMaximumWidth(150);
    PoseArray->addChild(PoseArrayTopic);
    treeWidget->setItemWidget(PoseArrayTopic, 1, PoseArray_Topic_box);

    hlayout->addWidget(qrviz);
    hlayout->addWidget(treeWidget);

    connect(Grid_Check, SIGNAL(clicked(bool)), this, SLOT(show_display_grid(bool)));
    connect(Map_Check, SIGNAL(clicked(bool)), this, SLOT(show_display_map(bool)));
    connect(Laser_Check, SIGNAL(clicked(bool)), this, SLOT(show_display_laser(bool)));
    connect(PoseArray_Check, SIGNAL(clicked(bool)), this, SLOT(show_display_posearray(bool)));
    connect(fixed_box, SIGNAL(editTextChanged(QString)), this, SLOT(show_display_fixed(QString)));
}

survey::~survey()
{
    delete ui;
}

void survey::show_display_fixed(QString topic)
{
    qrviz->Display_Fixed(topic);
}

void survey::show_display_grid(bool enable)
{
    qrviz->Display_Grid(enable);
}

void survey::show_display_map(bool enable)
{
    QString map_topic = Map_Topic_box->currentText();
    qrviz->Display_Map(enable, map_topic);

}

void survey::show_display_laser(bool enable)
{
    QString laser_topic = Laser_Topic_box->currentText();
    qrviz->Display_LaserScan(enable, laser_topic);
}

void survey::show_display_posearray(bool enable)
{
    QString posearray_topic = PoseArray_Topic_box->currentText();
    qrviz->Display_PoseArray(enable, posearray_topic);
}







