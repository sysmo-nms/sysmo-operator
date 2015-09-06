#include "stdio.h"
#include "stdlib.h"

#include "mainwindow.h"
#include "themes.h"
#include "sysmo.h"

#include <QApplication>
#include <QSettings>
#include <QIcon>
#include <QtGlobal>
#include <QStandardPaths>
#include <QSettings>
#include <QVariant>

void operatorMsgOut(
              QtMsgType           type,
        const QMessageLogContext &context,
        const QString            &msg)
{
    QByteArray localMsg = msg.toLocal8Bit();
    /*
    QString logDir = QStandardPath::writableLocation(
        QStandardPath::AppDataLocation)
    */
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

int main(int argc, char* argv[])
{

    int RETURN_CODE;
    do {

// see http://doc.qt.io/qt-5/qtglobal.html
#if !defined QT_DEBUG
    qputenv("QT_LOGGING_RULES", "qt.network.ssl.warning=false");
    qInstallMessageHandler(operatorMsgOut);
#endif

#if   defined Q_OS_MAC
    /* put mac things here*/
#elif defined Q_OS_WIN
    /* put windows things here*/
#else
    /* other OS/X11 things here */
#endif
            QApplication::setApplicationName("Operator");
            QApplication::setApplicationVersion("1.0");
            QApplication::setApplicationDisplayName("Sysmo Operator 1.0");
            QApplication::setOrganizationName("Sysmo NMS");
            QApplication::setOrganizationDomain("sysmo.io");
            QApplication::setQuitOnLastWindowClosed(true);
            QApplication::setStyle("fusion");

            QSettings settings;
            QVariant variant = settings.value("color_theme");
            if (!variant.isValid()) {
                    QApplication::setPalette(Themes::native);
            } else {
                    QString theme = variant.toString();
                    if (theme == "midnight") {
                            QApplication::setPalette(Themes::midnight);
                    } else if (theme == "inland") {
                            QApplication::setPalette(Themes::inland);
                    } else if (theme == "greys") {
                            QApplication::setPalette(Themes::greys);
                    } else if (theme == "iced") {
                            QApplication::setPalette(Themes::iced);
                    } else if (theme == "native") {
                            QApplication::setPalette(Themes::native);
                    }
            }

            QApplication app(argc, argv);
            app.setWindowIcon(QIcon(":/icons/logo.png"));

            MainWindow w;
            RETURN_CODE = app.exec();
    } while(RETURN_CODE == Sysmo::APP_RESTART_CODE);

    return RETURN_CODE;
}
