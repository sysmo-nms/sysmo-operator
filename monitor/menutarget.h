#ifndef MENUTARGET_H
#define MENUTARGET_H

#include "sysmo.h"
#include "monitor/monitor.h"
#include "dialogs/messagebox.h"
#include "network/supercast.h"
#include "network/supercastsignal.h"

#include <QObject>
#include <QWidget>
#include <QString>
#include <QMenu>
#include <QPoint>
#include <QAction>
#include <QIcon>
#include <QMessageBox>
#include <QJsonObject>

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
    void deleteTarget();
    void deleteTargetReply(QJsonObject reply);

signals:
    void openNewProbeDialog(QString target);
};

#endif // MENUTARGET_H
