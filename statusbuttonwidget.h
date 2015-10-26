#ifndef STATUSBUTTONWIDGET_H
#define STATUSBUTTONWIDGET_H

#include "nframecontainer.h"
#include "ngridcontainer.h"
#include "statusbutton.h"
#include "monitor/monitor.h"

#include <QWidget>
#include <QPixmap>
#include <QHash>
#include <QDebug>
#include <QJsonObject>
#include <QTimer>

class StatusButtonWidget : public NFrameContainer
{
    Q_OBJECT
public:
    StatusButtonWidget(QWidget* parent);
    StatusButton* ok;
    StatusButton* warn;
    StatusButton* crit;
    StatusButton* err;


private:
    QHash<QString, QString>* status_map;
    void incrementStatus(QString status);
    void decrementStatus(QString status);

public slots:
    void handleDeleteProbe(QJsonObject obj);
    void handleInfoProbe(QJsonObject obj);

};

#endif // STATUSBUTTONWIDGET_H
