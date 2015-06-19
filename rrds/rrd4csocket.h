#ifndef RRD4CSOCKET_H
#define RRD4CSOCKET_H

#include <QObject>
#include <QJsonDocument>
#include <QJsonObject>
#include <QStringList>
#include <QTcpSocket>
#include <QAbstractSocket>
#include <QDataStream>
#include <QHostAddress>
#include <QIODevice>
#include <Qt>

class Rrd4cSocket : public QObject
{
    Q_OBJECT

public:
    explicit Rrd4cSocket(QHostAddress host, qint16 port);
    ~Rrd4cSocket();
    QTcpSocket* socket = NULL;

public slots:
    void handleClientMessage(QJsonObject msg);

private:
    qint32 block_size;
    static const qint32 HEADER_LEN = 4;
    static qint32       arrayToInt32(QByteArray source);
    static QByteArray   int32ToArray(qint32 source);

private slots:
    void socketReadyRead();

signals:
    void serverMessage(QJsonObject msg);
};

#endif // RRD4CSOCKET_H
