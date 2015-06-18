#include "supercasthttpreply.h"

SupercastHttpReply::SupercastHttpReply()
{
    this->id   = 0;
    this->body = "empty";

}

SupercastHttpReply::SupercastHttpReply(int request_id, QString reply_body)
{
    this->id   = request_id;
    this->body = reply_body;
}

/*
SupercastHttpReply::SupercastHttpReply(const SupercastHttpReply &obj)
{
    this->id = obj.id;
    this->body = obj.body;
}


SupercastHttpReply::~SupercastHttpReply() {}

*/
