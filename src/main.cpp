#include "stdio.h"
#include "stdlib.h"

#include "include/mainwindow.h"
#include "include/themes.h"
#include "include/sysmo.h"

#include <QApplication>
#include <QSettings>
#include <QIcon>
#include <QtGlobal>
#include <QSettings>
#include <QVariant>

/*
 * TODO log system Qt4 compatible
 */
#if QT_VERSION >= 0x050000
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
#endif

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


                QString version = "1.1.0";

                QApplication::setApplicationName("Sysmo Operator");
                QApplication::setApplicationVersion(version);
                QApplication::setOrganizationName("Sysmo NMS");
                QApplication::setOrganizationDomain("sysmo.io");
                QApplication::setQuitOnLastWindowClosed(true);
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

#if QT_VERSION >= 0x050000
                QApplication::setStyle("fusion");
                qInstallMessageHandler(operatorMsgOut);
#else
                QApplication::setStyle("plastique");
#endif

                app.setWindowIcon(QIcon(":/icons/logo.png"));

                MainWindow w;

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