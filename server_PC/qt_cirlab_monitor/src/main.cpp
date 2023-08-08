#include "../include/qt_cirlab_monitor/mainwindow.hpp"
#include <QApplication>



int main(int argc, char** argv)
{
    ros::init(argc, argv, "qt_cirlab_monitor");
    QApplication a(argc, argv);
    monitor::MainWindow w(argc, argv);
    w.show();
    return a.exec();
}
