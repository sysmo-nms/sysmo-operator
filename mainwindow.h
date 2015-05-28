#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "centralwidget.h"

#include <QMainWindow>
#include <QIcon>
#include <QString>
#include <QLabel>
#include <QWidget>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = 0);
    ~MainWindow();
private:
    void initMenus();
    void initStatusBar();

};

#endif // MAINWINDOW_H
