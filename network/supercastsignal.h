#ifndef SUPERCASTSIGNAL_H
#define SUPERCASTSIGNAL_H

#include <QObject>
#include <QVariant>
#include <QString>

class SupercastSignal : public QObject
{
    Q_OBJECT

public:
    explicit SupercastSignal(QObject* parent = 0);

signals:
    void serverMessage(QVariant json);
    void serverMessage(QString  string);
    void serverMessage(int      integer);
};

#endif // SUPERCASTSIGNAL_H
