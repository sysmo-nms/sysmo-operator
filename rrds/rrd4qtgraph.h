#ifndef RRD4QTGRAPH_H
#define RRD4QTGRAPH_H

#include "rrds/rrd4qt.h"
#include "rrds/rrd4qtsignal.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QTemporaryFile>
#include <QPixmap>
#include <QDebug>
#include <QVariant>
#include <QMap>

class Rrd4QtGraph : public QLabel
{
    Q_OBJECT
public:
    explicit Rrd4QtGraph(
            QString     rrd_db_file,
            QMap<QString,QVariant> rrd_graph_config,
            int         initial_height,
            QWidget*    parent = 0);

private:
    QMap<QString,QVariant> graph_config;
    QString       graph_id;
    QString       pixmap_file;
    QPixmap       pixmap_obj;

public slots:
    void handleRrdReply(QVariant reply);
    void setTimeSpan(int time_span);
    void setGraphHeight(int height);
    void setGraphWidth(int width);
};

#endif // RRD4QTGRAPH_H
