#ifndef MAP_H
#define MAP_H

#include <QWidget>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <qwidget.h>
#include <qpushbutton.h>
#include <qlabel.h>
#include <qcombobox.h>
#include <qstring.h>
#include <QFrame>
#include <QSizePolicy>
#include <QLineEdit>
#include <qdebug.h>
#include <QGroupBox>
#include <QSpacerItem>
#include <QRadioButton>

namespace Ui {
class map;
}

class map : public QWidget
{
    Q_OBJECT

public:
    explicit map(QWidget *parent = 0);
    ~map();

//    QWidget *create_switch_map_button();
//    QWidget *create_current_map_text();
//    QWidget *create_goal_map_text();
    QGroupBox *create_avoidance();
    QGroupBox *create_navigation();
    QGroupBox *create_control();

private:
    Ui::map *ui;
    QLabel *current_map_label = new QLabel("Current Map:");
    QLabel *goal_map_label = new QLabel("Goal Map:");
    QPushButton *button_map1 = new QPushButton(tr("Forward"));
    QPushButton *button_map2 = new QPushButton(tr("Left"));
    QPushButton *button_map3 = new QPushButton(tr("Back"));
    QPushButton *button_map4 = new QPushButton(tr("Right"));
    QPushButton *button_map5 = new QPushButton(tr("Stop"));
    QLineEdit *current_map_lineedit = new QLineEdit();
    QComboBox *choose_map_combobox = new QComboBox();
    QString unpress_button_color = "background-color:#FB3232;"
                                   "border-radius:15px;"
                                   "border: 2px;"
                                   "border-color:#FB3232;";
    QString press_button_color = "background-color:#3BF169;"
                                 "border-radius:15px;"
                                 "border: 2px;"
                                 "border-color:#3BF169;";
    QString init_button_color = "background-color:#FB3232;"
                                "border-radius:15px;"
                                "border: 2px;"
                                "border-color:#FB3232;";
private slots:

    void button_map1_clicked();
    void button_map2_clicked();
    void button_map3_clicked();
    void button_map4_clicked();
    void button_map5_clicked();
};


#endif // MAP_H
