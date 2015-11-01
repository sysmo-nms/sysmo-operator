#ifndef MENUTARGET_H
#define MENUTARGET_H

#include "sysmo.h"
#include "monitor/monitor.h"
#include "dialogs/messagebox.h"
#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "actions/monitoractions.h"

#include <QObject>
#include <QWidget>
#include <QString>
#include <QMenu>
#include <QPoint>
#include <QAction>
#include <QIcon>
#include <QMessageBox>
#include <QVariant>
#include <QMap>

#include <QDebug>

class MenuTarget : public QMenu
{
    Q_OBJECT

public:
    MenuTarget(QWidget* parent = 0);
    void showMenuFor(QString target, QPoint at);

private:
    QString target_name;
    //QMenu*  operation_menu;

private slots:
    void connectNewProbeDialog();
    void deleteTarget();
    void deleteTargetReply(QVariant reply);
    void handleOperatorActionsConfig();

signals:
    void openNewProbeDialog(QString target);
};

#endif // MENUTARGET_H
