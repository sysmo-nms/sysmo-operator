#include "mainwindow.h"
#include "themes.h"

#include <QApplication>
#include <QSettings>
#include <QIcon>


int main(int argc, char* argv[])
{
    QApplication::setApplicationName("Operator");
    QApplication::setApplicationVersion("1.0");
    QApplication::setApplicationDisplayName("Sysmo Operator 1.0");
    QApplication::setOrganizationName("Sysmo IO");
    QApplication::setOrganizationDomain("sysmo.io");
    QApplication::setQuitOnLastWindowClosed(true);
    QApplication::setPalette(Themes::midnight);
    QApplication::setStyle("fusion");

    QApplication app(argc, argv);
    QApplication::setWindowIcon(QIcon(":/icons/logo.png"));

    MainWindow w;
    return app.exec();
}
