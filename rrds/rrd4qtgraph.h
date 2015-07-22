#ifndef RRD4QTGRAPH_H
#define RRD4QTGRAPH_H

#include "rrds/rrd4qt.h"
#include "rrds/rrd4qtsignal.h"

#include <QObject>
#include <QWidget>
#include <QLabel>
#include <QJsonObject>
#include <QJsonValue>
#include <QTemporaryFile>
#include <QDebug>

class Rrd4QtGraph : public QLabel
{
    Q_OBJECT
public:
    explicit Rrd4QtGraph(
            QString     rrd_db_file,
            QJsonObject rrd_graph_config,
            QWidget*    parent = 0);

private:
    QJsonObject graph_config;
    QString     graph_id;

public slots:
    void handleRrdReply(QJsonObject reply);
};

#endif // RRD4QTGRAPH_H
