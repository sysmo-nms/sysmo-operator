#ifndef STATUSBUTTONWIDGET_H
#define STATUSBUTTONWIDGET_H

#include "include/nframecontainer.h"
#include "include/ngridcontainer.h"
#include "include/statusbutton.h"
#include "include/monitor/monitor.h"

#include <QWidget>
#include <QPixmap>
#include <QMap>
#include <QDebug>
#include <QTimer>
#include <QVariant>

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
    QMap<QString, QString>* status_map;
    void incrementStatus(QString status);
    void decrementStatus(QString status);

public slots:
    void handleDeleteProbe(QVariant obj);
    void handleInfoProbe(QVariant obj);

};

#endif // STATUSBUTTONWIDGET_H