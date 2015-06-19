#ifndef RRD4CSIGNAL_H
#define RRD4CSIGNAL_H

#include <QObject>
#include <QJsonObject>

class Rrd4cSignal : public QObject
{
    Q_OBJECT

public:
    explicit Rrd4cSignal(QObject* parent = 0);

signals:
    void serverMessage(QJsonObject json);
    void serverMessage(QString     string);
    void serverMessage(int         integer);
};

#endif // RRD4CSIGNAL_H
