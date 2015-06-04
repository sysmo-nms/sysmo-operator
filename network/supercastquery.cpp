#include "supercastquery.h"

SupercastQuery::SupercastQuery(QObject* parent) : QObject(parent)
{

}

SupercastQuery::~SupercastQuery()
{
    delete this->json_query;
}


void SupercastQuery::setQuery(QJsonObject query)
{
    this->json_query = new QJsonObject(query);
}


void SupercastQuery::apply()
{
    // Supercast::sendQuery(this);

}
