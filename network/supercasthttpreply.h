#ifndef SUPERCASTHTTPREPLY_H
#define SUPERCASTHTTPREPLY_H

#include <QString>

class SupercastHttpReply
{
public:
    /*
     * Default constructor for qRegisterMetaType?
     */
    SupercastHttpReply();
    SupercastHttpReply(int request_id, QString reply_body);
    int     id;
    QString body;
};

#endif // SUPERCASTHTTPREPLY_H
