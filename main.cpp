#include "mainwindow.h"

#include <QApplication>
#include <QString>
#include <QPalette>

int main(int argc, char *argv[])
{

    // the reverse do not keep the original palette
    /*
    QApplication::setStyle(QString("fusion"));
    QApplication a(argc, argv);
    */

    // this keep the original palette
    QApplication a(argc, argv);
    QApplication::setStyle(QString("fusion"));
    MainWindow w;
    w.show();

    return a.exec();
}
