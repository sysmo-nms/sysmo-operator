#ifndef SUPERCASTHTTPREQUEST_H
#define SUPERCASTHTTPREQUEST_H

#include <QUrl>

class SupercastHttpRequest
{
public:
    /*
     * Default constructor for qRegisterMetaType
     */
    SupercastHttpRequest();
    SupercastHttpRequest(int request_id, QUrl request_url);
    int  id;
    QUrl url;
};

#endif // SUPERCASTHTTPREQUEST_H
