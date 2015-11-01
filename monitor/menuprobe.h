#ifndef MENUPROBE_H
#define MENUPROBE_H

#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "windows/probewindow.h"
#include "dialogs/messagebox.h"

#include <QMenu>
#include <QWidget>
#include <QString>
#include <QPoint>
#include <QAction>

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
    void handleForceProbeReply(QJsonObject reply);
    void handlePauseProbe();
    void handleDeleteProbe();
    void handleDeleteProbeReply(QJsonObject reply);
    void handleShowPerf();

};

#endif // MENUPROBE_H
