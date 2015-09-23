#ifndef MONITORLOGS_H
#define MONITORLOGS_H

#include "nframe.h"
#include "ngridcontainer.h"

#include <QWidget>
#include <QFrame>
#include <QTextEdit>
#include <QJsonObject>

#include <QDebug>

class MonitorLogs : public NFrame
{

    Q_OBJECT
public:
    explicit MonitorLogs(QWidget* parent = 0);

public slots:
    void probeReturn(QJsonObject obj);

private:
    QTextEdit* logarea;
    static MonitorLogs* singleton;
};

#endif // MONITORLOGS_H
