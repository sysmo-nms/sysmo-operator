#include "mainwindow.h"

#include <QApplication>
#include <QString>

int main(int argc, char *argv[])
{
    QApplication::setStyle(QString("fusion"));
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
