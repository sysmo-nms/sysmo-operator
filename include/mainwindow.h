/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
*/
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "include/centralwidget.h"
#include "include/dialogs/login.h"
#include "include/network/supercast.h"
#include "include/rrds/rrd4qt.h"
#include "include/dialogs/messagebox.h"
#include "include/systemtray.h"

#include <QMainWindow>
#include <QIcon>
#include <QWidget>
#include <QAction>
#include <QActionGroup>
#include <QMenuBar>
#include <QMenu>
#include <QKeySequence>
#include <QObject>
#include <QHostAddress>
#include <QMessageBox>
#include <QAbstractSocket>
#include <QSize>
#include <QCoreApplication>
#include <QDesktopServices>
#include <QUrl>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget* parent = 0);
    ~MainWindow();
    QWidget* getLoginWindow();
    QSize sizeHint() const;

public slots:
    void connectionStatus(int status);

private:
    void restoreStateFromSettings();
    Supercast* supercast;
    LogIn* log_in_dialog;
    Rrd4Qt* rrd4c;
    QActionGroup* color_group;
    SystemTray* system_tray;
    QSize default_size;

private slots:
    void toggleFullScreen();
    void tryValidate();
    void setThemeConfig(QAction* theme);
    void configureDocEngine();
    void handleHelpAction();
    void handleMainWebsiteAction();
    void handleAboutAction();
};

#endif // MAINWINDOW_H
