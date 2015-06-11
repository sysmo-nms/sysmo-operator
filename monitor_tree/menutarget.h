#ifndef MENUTARGET_H
#define MENUTARGET_H

#include "dialogs/newprobe.h"

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
    MenuTarget(QWidget* parent);
    void showMenuFor(QString target, QPoint at);

private:
    QString target_name = "";
    QMenu*  operation_menu = NULL;
    NewProbe* probe_dialog = NULL;
};

#endif // MENUTARGET_H
