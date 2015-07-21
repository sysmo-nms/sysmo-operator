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
