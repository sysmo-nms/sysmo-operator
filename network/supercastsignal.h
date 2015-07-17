#ifndef SUPERCASTSIGNAL_H
#define SUPERCASTSIGNAL_H

#include <QObject>
#include <QJsonObject>

class SupercastSignal : public QObject
{
    Q_OBJECT

public:
    explicit SupercastSignal();

signals:
    void serverMessage(QJsonObject json);
    void serverMessage(QString     string);
    void serverMessage(int         integer);
};

#endif // SUPERCASTSIGNAL_H
