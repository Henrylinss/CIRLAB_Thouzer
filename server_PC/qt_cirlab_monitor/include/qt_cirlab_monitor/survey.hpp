#ifndef SURVEY_H
#define SURVEY_H

#include "mainwindow.hpp"
#include "qrviz.hpp"
#include <QWidget>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QFrame>
#include <QComboBox>
#include <QSizePolicy>
#include <QLineEdit>
#include <QGroupBox>
#include <QSpacerItem>
#include <QTreeWidgetItem>
#include <QCheckBox>
#include <QSpinBox>

namespace Ui {
class survey;
}

class survey : public QWidget
{
    Q_OBJECT

public:
    explicit survey(QWidget *parent = 0);
    ~survey();

private:
    Ui::survey *ui;
    QRviz* qrviz = NULL;
    QComboBox* fixed_box;
    QComboBox* Grid_Color_Box;
    QComboBox* Laser_Topic_box;
    QComboBox* Map_Topic_box;
    QComboBox* PoseArray_Topic_box;
    QCheckBox* Map_Check;
    QCheckBox* Laser_Check;
    QCheckBox* Grid_Check;
    QCheckBox* PoseArray_Check;


private slots:
    void show_display_grid(bool);
    void show_display_map(bool);
    void show_display_laser(bool);
    void show_display_posearray(bool);
    void show_display_fixed(QString);

};

#endif // SURVEY_H
