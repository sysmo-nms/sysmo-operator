#include "mainwindow.h"
#include "themes.h"

#include <QApplication>
#include <QPalette>
#include <QSettings>
#include <QIcon>
#include <Qt>


int main(int argc, char* argv[])
{
    QApplication::setApplicationName("Operator");
    QApplication::setApplicationVersion("1.0");
    QApplication::setApplicationDisplayName("Sysmo Operator 1.0");
    QApplication::setOrganizationName("Sysmo IO");
    QApplication::setOrganizationDomain("sysmo.io");
    QApplication::setQuitOnLastWindowClosed(true);
    QApplication::setPalette(Themes::native);
    QApplication::setStyle("fusion");

    QApplication app(argc, argv);
    QApplication::setWindowIcon(QIcon(":/icons/logo.png"));
    MainWindow   main_window;
    return app.exec();
}
