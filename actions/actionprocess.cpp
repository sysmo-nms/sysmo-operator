#include "actionprocess.h"

ActionProcess::ActionProcess(QObject *parent)
    : QProcess(parent)
{
    QObject::connect(
                this, SIGNAL(finished(int)),
                this, SLOT(deleteLater()));

    QObject::connect(
                this, SIGNAL(error(QProcess::ProcessError)),
                this, SLOT(handleStartError(QProcess::ProcessError)));

    QObject::connect(
                this, SIGNAL(readyReadStandardError()),
                this, SLOT(handleErrorMsg()));

}

void ActionProcess::handleStartError(QProcess::ProcessError err)
{
    QString str;
    str += this->program();
    str += " ";
    str += this->arguments().join(" ");
    str += "\n\n";

    switch(err) {
    case QProcess::FailedToStart:
        str += "The process failed to start. Either the invoked program is missing, or you may have insufficient permissions to invoke the program.";
        break;
    case QProcess::Crashed:
        str += "The process crashed some time after starting successfully.";
        break;
    case QProcess::Timedout:
        str += "The last waitFor...() function timed out. The state of QProcess is unchanged, and you can try calling waitFor...() again.";
        break;
    case QProcess::WriteError:
        str += "An error occurred when attempting to write to the process. For example, the process may not be running, or it may have closed its input channel.";
        break;
    case QProcess::ReadError:
        str += "An error occurred when attempting to read from the process. For example, the process may not be running.";
        break;
    default:
        str += "An unknown error occurred. This is the default return value of error().";
        break;
    }


    SystemTray::singleton->showMessage("Start action error", str,
                                       QSystemTrayIcon::Critical, 10000);
}

void ActionProcess::handleErrorMsg()
{
    this->error_string += QString(this->readAllStandardError());

    QString str;
    str += this->program();
    str += " ";
    str += this->arguments().join(" ");
    str += "\n\n";
    str += this->error_string;

    SystemTray::singleton->showMessage(
                "Start action stderr msg", str,
                                       QSystemTrayIcon::Warning, 5000);
}