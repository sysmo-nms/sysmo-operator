#include "mainwindow.h"
#include "themes.h"

#include <QApplication>
#include <QSettings>
#include <QIcon>


int main(int argc, char* argv[])
{

// see http://doc.qt.io/qt-5/qtglobal.html
#ifndef QT_DEBUG
    qputenv("QT_LOGGING_RULES", "qt.network.ssl.warning=false");
#endif

    QApplication::setApplicationName("Operator");
    QApplication::setApplicationVersion("1.0");
    QApplication::setApplicationDisplayName("Sysmo Operator 1.0");
    QApplication::setOrganizationName("Sysmo IO");
    QApplication::setOrganizationDomain("sysmo.io");
    QApplication::setQuitOnLastWindowClosed(true);
#ifndef Q_OS_MAC
    QApplication::setPalette(Themes::midnight);
    QApplication::setStyle("fusion");
#endif

    QApplication app(argc, argv);
    QApplication::setWindowIcon(QIcon(":/icons/logo.png"));

    MainWindow w;
    return app.exec();
}
