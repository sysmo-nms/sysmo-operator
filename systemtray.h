#ifndef SYSTEMTRAY_H
#define SYSTEMTRAY_H

#include <QObject>
#include <QWidget>
#include <QSystemTrayIcon>
#include <QIcon>

class SystemTray : public QSystemTrayIcon
{
    Q_OBJECT
public:
    explicit SystemTray(QObject *parent = 0);

public:
    static SystemTray *singleton;
};

#endif // SYSTEMTRAY_H
