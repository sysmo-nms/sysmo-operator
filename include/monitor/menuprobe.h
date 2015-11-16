#ifndef MENUPROBE_H
#define MENUPROBE_H

#include "include/network/supercast.h"
#include "include/network/supercastsignal.h"
#include "include/windows/probewindow.h"
#include "include/dialogs/messagebox.h"

#include <QMenu>
#include <QWidget>
#include <QString>
#include <QPoint>
#include <QAction>
#include <QVariant>
#include <QMap>

#include <QDebug>


class MenuProbe : public QMenu
{
    Q_OBJECT

public:
    MenuProbe(QWidget* parent = 0);
    void showMenuFor(QString target, QPoint at);

private:
    QString probe_name;

private slots:
    void handleForceProbe();
    void handleForceProbeReply(QVariant reply);
    void handlePauseProbe();
    void handleDeleteProbe();
    void handleDeleteProbeReply(QVariant reply);
    void handleShowPerf();

};

#endif // MENUPROBE_H