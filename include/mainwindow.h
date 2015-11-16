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
