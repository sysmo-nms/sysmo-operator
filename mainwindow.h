#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "iostream"

#include "centralwidget.h"
#include "dialogs/login.h"
#include "network/supercast.h"

#include <QMainWindow>
#include <QIcon>
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
#include <QHostAddress>
#include <QDialog>
#include <QMessageBox>
#include <QAbstractSocket>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget* parent = 0);
    ~MainWindow();

public slots:
    void connexionStatus(int status);

private:
    LogIn* log_in_dialog;

private slots:
    void toggleFullScreen();
    void tryValidate();
};

#endif // MAINWINDOW_H
