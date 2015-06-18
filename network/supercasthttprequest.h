#ifndef SUPERCASTHTTPREQUEST_H
#define SUPERCASTHTTPREQUEST_H

#include <QString>

class SupercastHttpRequest
{
public:
    /*
     * Default constructor for qRegisterMetaType
     */
    SupercastHttpRequest();
    SupercastHttpRequest(int request_id, QString request_url);
    int     id;
    QString url;
};

#endif // SUPERCASTHTTPREQUEST_H
