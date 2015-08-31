#ifndef ACTIONPROCESS_H
#define ACTIONPROCESS_H

#include <QObject>
#include <QProcess>
#include <QDebug>

class ActionProcess : public QProcess
{
    Q_OBJECT
public:
    ActionProcess(QObject *parent = 0);

private:
    QString error_string;

private slots:
    void handleErrorMsg();
    void handleError(int ret);
};

#endif // ACTIONPROCESS_H
