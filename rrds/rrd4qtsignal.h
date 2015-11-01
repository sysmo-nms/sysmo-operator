#ifndef RRD4QTSIGNAL_H
#define RRD4QTSIGNAL_H

#include <QObject>
#include <QVariant>
#include <QString>

class Rrd4QtSignal : public QObject
{
    Q_OBJECT

public:
    explicit Rrd4QtSignal(QObject* parent = 0);

signals:
    void serverMessage(QVariant json);
    void serverMessage(QString  string);
    void serverMessage(int      integer);
};

#endif // RRD4QTSIGNAL_H
