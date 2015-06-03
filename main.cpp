#include "mainwindow.h"

#include <QApplication>
#include <QString>
#include <QPalette>

QPalette native_palette;
QPalette undef_palette;


/*
 * Fake start used to fetch the native palette from
 * an initialized QApplication.
 */
void fake_start(int argc, char* argv[])
{

    undef_palette  = QPalette();
    QApplication a(argc, argv);
    native_palette = QPalette(a.palette());
}


int main(int argc, char* argv[])
{

    fake_start(argc, argv);
    QApplication::setStyle(QString("fusion"));
    QApplication::setPalette(native_palette);

    QApplication a(argc, argv);
    MainWindow w;

    return a.exec();
}
