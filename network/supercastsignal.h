#ifndef SUPERCASTSIGNAL_H
#define SUPERCASTSIGNAL_H

#include <QObject>
#include <QJsonObject>

class SupercastSignal : public QObject
{
    Q_OBJECT

public:
    explicit SupercastSignal(QObject* parent = 0);

signals:
    void sendMessage(QJsonObject json);
};

#endif // SUPERCASTSIGNAL_H
