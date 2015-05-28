#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowIcon(QIcon(":/ressources/images/32/logo.png"));
    setWindowTitle(QString("Sysmo Operator"));
    setObjectName("MainWindow");
    setCentralWidget(new CentralWidget(this));
}

void MainWindow::initMenus()
{

}

void MainWindow::initStatusBar()
{

}

MainWindow::~MainWindow()
{

}
