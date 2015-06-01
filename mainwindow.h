#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "centralwidget.h"
#include "dialogs/login.h"
#include "network/supercast.h"

#include <QMainWindow>
#include <QIcon>
#include <QString>
#include <QLabel>
#include <QWidget>
#include <QAction>
#include <QActionGroup>
#include <QMenuBar>
#include <QMenu>
#include <QStatusBar>
#include <QIcon>
#include <QKeySequence>
#include <QObject>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
public slots:
    void toggleFullScreen();
private:
    LogIn *log_in_dialog;
    Supercast *supercast;

};

#endif // MAINWINDOW_H
