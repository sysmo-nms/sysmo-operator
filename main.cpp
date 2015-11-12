#include "stdio.h"
#include "stdlib.h"

#include "mainwindow.h"
#include "themes.h"
#include "sysmo.h"

#include <QApplication>
#include <QSettings>
#include <QIcon>
#include <QtGlobal>
#include <QSettings>
#include <QVariant>
#include <QStringList>
#include <QLibraryInfo>

//#include <QSplashScreen>
//#include <QPixmap>

/* Qt4 incompatible
 * TODO log system
 */
/*
void operatorMsgOut(
              QtMsgType           type,
        const QMessageLogContext &context,
        const QString            &msg)
{
    QByteArray localMsg = msg.toLocal8Bit();
    //QString logDir = QDesktopServices::writableLocation(
        //QDesktopServices::AppDataLocation)
    switch (type) {
    case QtDebugMsg:
        fprintf(stderr, "Debug: %s (%s:%u, %s)\n",
                localMsg.constData(),
                context.file,
                context.line,
                context.function);
        break;
    case QtWarningMsg:
        fprintf(stderr, "Warning: %s (%s:%u, %s)\n",
                localMsg.constData(),
                context.file,
                context.line,
                context.function);
        break;
    case QtCriticalMsg:
        fprintf(stderr, "Critical: %s (%s:%u, %s)\n",
                localMsg.constData(),
                context.file,
                context.line,
                context.function);
        break;
    case QtFatalMsg:
        fprintf(stderr, "Fatal: %s (%s:%u, %s)\n",
                localMsg.constData(),
                context.file,
                context.line,
                context.function);
        abort();
    default:
        break;
    }
}
*/


int main(int argc, char* argv[])
{

        int RETURN_CODE;
        do {
// see http://doc.qt.io/qt-5/qtglobal.html
#if !defined QT_DEBUG
    qputenv("QT_LOGGING_RULES", "qt.network.ssl.warning=false");
#endif

#if   defined Q_OS_MAC
    /* put mac things here*/
#elif defined Q_OS_WIN
    /* put windows things here*/
#else
    /* other OS/X11 things here */
#endif

                //qInstallMessageHandler(operatorMsgOut); TODO C++ qt4 compatible log system

                QString version = "1.1.0";

                QApplication::setApplicationName("Sysmo Operator");
                QApplication::setApplicationVersion(version);
                QApplication::setOrganizationName("Sysmo NMS");
                QApplication::setOrganizationDomain("sysmo.io");
                QApplication::setQuitOnLastWindowClosed(true);
#if QT_VERSION >= 0x050000
                QApplication::setStyle("fusion");
#else
                QApplication::setStyle("plastique");
#endif
                QSettings settings;
                QVariant variant = settings.value("color_theme");
                if (variant.isValid()) {
                        QString theme = variant.toString();
                        if (theme == "midnight") {
                                QApplication::setPalette(Themes::midnight);
                        } else if (theme == "inland") {
                                QApplication::setPalette(Themes::inland);
                        } else if (theme == "greys") {
                                QApplication::setPalette(Themes::greys);
                        } else if (theme == "iced") {
                                QApplication::setPalette(Themes::iced);
                        }
                }

                QApplication app(argc, argv);

                qDebug() << "will look for plugins in: "
                         << QLibraryInfo::location(QLibraryInfo::PluginsPath);
                qDebug() << "will look for libraries in: "
                         << QLibraryInfo::location(QLibraryInfo::LibrariesPath);
                app.setWindowIcon(QIcon(":/icons/logo.png"));
                //QPixmap pixmap(":/images/banner.png");
                //QSplashScreen splash(pixmap);
                //splash.show();
                //app.processEvents();

                MainWindow w;

                //splash.finish(w.getLoginWindow());
                w.initSysmo();

                RETURN_CODE = app.exec();
#if QT_VERSION < 0x050000
                if (RETURN_CODE == Sysmo::APP_RESTART_CODE) {
                    // TODO make app restart working with qt4
                    RETURN_CODE = 0;
                }
#endif
        } while (RETURN_CODE == Sysmo::APP_RESTART_CODE);

        return RETURN_CODE;
}
