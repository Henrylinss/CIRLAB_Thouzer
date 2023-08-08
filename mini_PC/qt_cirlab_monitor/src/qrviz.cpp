#include "../include/qt_cirlab_monitor/qrviz.hpp"
#include <QTimer>

QRviz::QRviz(QWidget *parent):
    QWidget(parent)
{
    render_panel_ = new rviz::RenderPanel;
    render_panel_->setFixedSize(400, 450);
    QVBoxLayout* vlayout = new QVBoxLayout;
    vlayout->addWidget(render_panel_);
    setLayout(vlayout); 
    manager_ = new rviz::VisualizationManager(render_panel_);
    render_panel_->initialize(manager_->getSceneManager(),manager_);

    manager_->initialize();
    manager_->removeAllDisplays();
    manager_->startUpdate();


}

void QRviz::Display_Fixed(QString topic)
{
    manager_->setFixedFrame(topic);
    manager_->startUpdate();
}

void QRviz::Display_Grid(bool enable, QColor color)
{
    if (grid_ == NULL) {
        grid_ = manager_->createDisplay("rviz/Grid", "adjustable grid", true);
        ROS_ASSERT(grid_ != NULL);
        // Configure the GridDisplay the way we like it.
        grid_->subProp("Line Style")->setValue("Billboards");
        grid_->subProp("Color")->setValue(color);
    }
    else {
        delete grid_;
        grid_ = manager_->createDisplay("rviz/Grid", "adjustable grid", true);
        ROS_ASSERT(grid_ != NULL);
        // Configure the GridDisplay the way we like it.
        grid_->subProp("Line Style")->setValue("Billboards");
        grid_->subProp("Color")->setValue(color);
    }
    grid_->setEnabled(enable);
    manager_->startUpdate();
}

void QRviz::Display_Map(bool enable, QString topic)
{
    if (!enable && map_) {
        map_->setEnabled(false);
        return;
    }
    if (map_ == NULL) {
        map_ = manager_->createDisplay("rviz/Map", "QMap", true);
        ROS_ASSERT(map_);
        map_->subProp("Topic")->setValue(topic);
    }
    else {
        delete map_;
        map_ = manager_->createDisplay("rviz/Map", "QMap", true);
        ROS_ASSERT(map_);
        map_->subProp("Topic")->setValue(topic);
    }

    map_->setEnabled(enable);
    manager_->startUpdate();
}

void QRviz::Display_LaserScan(bool enable, QString topic, QColor color) {
    if (laser_ == NULL) {
        laser_ = manager_->createDisplay("rviz/LaserScan", "QLaser", enable);
        ROS_ASSERT(laser_);
        laser_->subProp("Topic")->setValue(topic);
        laser_->subProp("Color")->setValue(color);
        laser_->subProp("Queue Size")->setValue(10);
    }
    else {
        delete laser_;
        laser_ = manager_->createDisplay("rviz/LaserScan", "QLaser", enable);
        ROS_ASSERT(laser_);
        laser_->subProp("Topic")->setValue(topic);
        laser_->subProp("Color")->setValue(color);
        laser_->subProp("Queue Size")->setValue(10);
    }
    laser_->setEnabled(enable);
    manager_->startUpdate();
}

void QRviz::Display_PoseArray(bool enable, QString topic, QColor color)
{
    if (posearray_ == NULL) {
            posearray_ = manager_->createDisplay("rviz/PoseArray", "QPoseArray", enable);
            ROS_ASSERT(posearray_);
            posearray_->subProp("Topic")->setValue(topic);
            posearray_->subProp("Color")->setValue(color);
        }
    else {
        delete posearray_;
        posearray_ = manager_->createDisplay("rviz/PoseArray", "QPoseArray", enable);
        ROS_ASSERT(posearray_);
        posearray_->subProp("Topic")->setValue(topic);
        posearray_->subProp("Color")->setValue(color);
    }
    posearray_->setEnabled(enable);
    manager_->startUpdate();
}






QRviz::~QRviz()
{
    delete manager_;
}



