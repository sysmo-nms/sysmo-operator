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
    SupercastHttpRequest(int request_id, QString dst_file, QUrl request_url);
    QString dst_file = "none";
    int  id;
    QUrl url;
};

#endif // SUPERCASTHTTPREQUEST_H
