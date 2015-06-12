#ifndef MENUTARGET_H
#define MENUTARGET_H

#include "monitor/monitor.h"

#include <QObject>
#include <QWidget>
#include <QString>
#include <QMenu>
#include <QPoint>
#include <QAction>
#include <QIcon>

#include <QDebug>

class MenuTarget : public QMenu
{
    Q_OBJECT

public:
    MenuTarget(QWidget* parent = 0);
    void showMenuFor(QString target, QPoint at);

private:
    QString target_name = "";
    QMenu*  operation_menu = NULL;

private slots:
    void connectNewProbeDialog();

signals:
    void openNewProbeDialog(QString target);
};

#endif // MENUTARGET_H
