#include "actionprocess.h"

ActionProcess::ActionProcess(QObject *parent)
    : QProcess(parent)
{
    // TODO loguer les erreurs dans une bulle systeme
    QObject::connect(
                this, SIGNAL(finished(int)),
                this, SLOT(deleteLater()));

    //qRegisterMetaType<QProcess::ProcessError>();
    QObject::connect(
                this, SIGNAL(finished(int)),
                this, SLOT(handleError(int)));

    QObject::connect(
                this, SIGNAL(readyReadStandardError()),
                this, SLOT(handleErrorMsg()));

}


void ActionProcess::handleErrorMsg()
{
    this->error_string += QString(this->readAllStandardError());
}

void ActionProcess::handleError(int ret)
{
    qDebug() << "Exit with return status " << ret;
    qDebug() << this->error_string;
}
