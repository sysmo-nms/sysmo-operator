#ifndef SUPERCASTHTTP_H
#define SUPERCASTHTTP_H

#include <QObject>
#include <QString>
#include <QXmlSimpleReader>
#include <QXmlInputSource>

#include <QDebug>

class SupercastHTTP : public QObject
{
    Q_OBJECT

public:
    explicit SupercastHTTP(QObject* parent = 0);
    ~SupercastHTTP();

public slots:
    void handleClientRequest(QString url);

signals:
    void serverReply(QString body);
};

#endif // SUPERCASTHTTP_H
