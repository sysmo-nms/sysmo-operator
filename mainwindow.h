#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "centralwidget.h"
#include "dialogs/login.h"
#include "network/supercast.h"
#include "rrds/rrd4c.h"
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
    Supercast* supercast     = NULL;
    LogIn*     log_in_dialog = NULL;
    Rrd4c*     rrd4c         = NULL;
    QSize default_size;

private slots:
    void toggleFullScreen();
    void tryValidate();
};

#endif // MAINWINDOW_H
