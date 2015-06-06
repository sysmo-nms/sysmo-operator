#include "mainwindow.h"
#include "themes.h"

#include <QApplication>
#include <QPalette>
#include <QSettings>
#include <QIcon>
#include <Qt>

QPalette get_palette(int argc, char* argv[])
{
    // get native palette
    QApplication fake(argc, argv);
    QPalette native = QPalette(fake.palette());

    // TODO check QSettings
    return Themes::midnight;
    //QApplication::setDesktopSettingsAware(true);
    //return native;
}


int main(int argc, char* argv[])
{
    QApplication::setApplicationName("Operator");
    QApplication::setApplicationVersion("1.0");
    QApplication::setApplicationDisplayName("Sysmo Operator 1.0");
    QApplication::setOrganizationName("Sysmo IO");
    QApplication::setOrganizationDomain("sysmo.io");
    QApplication::setWindowIcon(QIcon(":/ressources/icons/32/logo.png"));
    QApplication::setQuitOnLastWindowClosed(true);

    QApplication::setPalette(get_palette(argc, argv));
    QApplication::setStyle("fusion");

    QApplication app(argc, argv);

    MainWindow w;

    return app.exec();
}
