#ifndef ACTIONPROCESS_H
#define ACTIONPROCESS_H

#include "include/systemtray.h"

#include <QObject>
#include <QProcess>
#include <QDebug>
#include <QSystemTrayIcon>

class ActionProcess : public QProcess
{
    Q_OBJECT
public:
    ActionProcess(QObject *parent = 0);
    void startProcess(const QString program, const QStringList arguments);

private:
    QString error_string;
    QString programString;
    QStringList programArgs;

private slots:
    void handleErrorMsg();
    void handleStartError(QProcess::ProcessError);
};

#endif // ACTIONPROCESS_H
