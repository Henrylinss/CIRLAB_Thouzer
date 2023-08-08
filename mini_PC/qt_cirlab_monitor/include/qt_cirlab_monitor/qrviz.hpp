#ifndef QRVIZ_H
#define QRVIZ_H

#include <rviz/visualization_manager.h>
#include <rviz/render_panel.h>
#include <rviz/display.h>
#include <rviz/tool_manager.h>
#include <rviz/tool.h>

#include <QWidget>
#include <QDebug>
#include <QException>
#include <QThread>
#include <QVBoxLayout>

namespace rviz {
    class Display;
    class RenderPanel;
    class VisualizationManager;
}


class QRviz : public QWidget {
  Q_OBJECT

public:
      QRviz(QWidget *parent = 0);
      virtual ~QRviz();
      void Display_IMAGE();
      void Display_Fixed(QString topic = "/map");
      void Display_Grid(bool enable = false, QColor color = QColor(125, 125, 125));
      void Display_Map(bool enable = false, QString topic = "/map");
      void Display_LaserScan(bool enable = false, QString topic = "/scan", QColor color = QColor(0, 0, 127));
      void Display_PoseArray(bool enable = false, QString topic = "/particlecloud", QColor color = QColor(225, 25, 0));

private:
      rviz::RenderPanel* render_panel_;
      rviz::VisualizationManager* manager_;
      rviz::Display* grid_ = NULL;
      rviz::Display* map_ = NULL;
      rviz::Display* laser_ = NULL;
      rviz::Display* posearray_ = NULL;

};

#endif  // QRVIZ_H
