#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "centralwidget.h"
#include "dialogs/login.h"
#include "network/supercast.h"
#include "rrds/rrd4qt.h"
#include "dialogs/messagebox.h"

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

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget* parent = 0);
    ~MainWindow();
    QSize sizeHint() const;

public slots:
    void connectionStatus(int status);

private:
    void restoreUserSettings();
    Supercast* supercast      = NULL;
    LogIn* log_in_dialog      = NULL;
    Rrd4Qt* rrd4c             = NULL;
    QActionGroup* color_group = NULL;
    QSize default_size;

private slots:
    void toggleFullScreen();
    void tryValidate();
    void setThemeConfig(QAction* theme);
};

#endif // MAINWINDOW_H
