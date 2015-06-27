#ifndef ABSTRACTCHANNEL_H
#define ABSTRACTCHANNEL_H

#include <QObject>

class AbstractChannel : public QObject
{
    Q_OBJECT
public:
    explicit AbstractChannel(QObject *parent = 0);

signals:

public slots:
};

#endif // ABSTRACTCHANNEL_H
