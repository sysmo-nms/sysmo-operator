#include "stdio.h"
#include "stdlib.h"

#include "mainwindow.h"
#include "themes.h"

#include <QApplication>
#include <QSettings>
#include <QIcon>
#include <QtGlobal>

void operatorMsgOut(
              QtMsgType           type,
        const QMessageLogContext &context,
        const QString            &msg)
{
    QByteArray localMsg = msg.toLocal8Bit();
    switch (type) {
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

// see http://doc.qt.io/qt-5/qtglobal.html
#if !defined QT_DEBUG
    qputenv("QT_LOGGING_RULES", "qt.network.ssl.warning=false");
    qInstallMessageHandler(operatorMsgOut);
#endif

#if   defined Q_OS_MAC
    /* put mac things here*/
#elif defined Q_OS_WIN
    /* put windows things here*/
    QApplication::setPalette(Themes::native);
    QApplication::setStyle("fusion");
#else
    /* other OS/X11 things here */
    QApplication::setPalette(Themes::midnight);
    QApplication::setStyle("fusion");
#endif

    QApplication::setApplicationName("Operator");
    QApplication::setApplicationVersion("1.0");
    QApplication::setApplicationDisplayName("Sysmo Operator 1.0");
    QApplication::setOrganizationName("Sysmo NMS");
    QApplication::setOrganizationDomain("sysmo.io");
    QApplication::setQuitOnLastWindowClosed(true);

    QApplication app(argc, argv);
    app.setWindowIcon(QIcon(":/icons/logo.png"));

    MainWindow w;

    return app.exec();
}
