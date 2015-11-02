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
    void emitServerMessage(QVariant json);
    void emitServerMessage(QString string);
    void emitServerMessage(int integer);

signals:
    void serverMessage(QVariant json);
    void serverMessage(QString  string);
    void serverMessage(int      integer);
};

#endif // SUPERCASTSIGNAL_H
