#include "include/systemtray.h"

SystemTray* SystemTray::singleton = NULL;

SystemTray::SystemTray(QObject *parent)
    : QSystemTrayIcon(parent)
{
    SystemTray::singleton = this;
    //this->setContextMenu(new QMenu());
    this->setIcon(QIcon(":icons/logo.png"));
    this->show();
}
