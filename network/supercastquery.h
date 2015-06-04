#ifndef SUPERCASTQUERY_H
#define SUPERCASTQUERY_H

#include <QObject>
#include <QJsonObject>

class SupercastQuery : public QObject
{
    Q_OBJECT

public:
    explicit SupercastQuery(QObject *parent = 0);
    ~SupercastQuery();
    void setQuery(QJsonObject query);
    void apply();

private:
    QJsonObject* json_query;


signals:
    void reply(QJsonObject reply);
};

#endif // SUPERCASTQUERY_H
