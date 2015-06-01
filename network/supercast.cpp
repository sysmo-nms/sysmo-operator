#include "supercast.h"

Supercast::Supercast(QObject *parent) : QObject(parent)
{

    supercast_socket = new SupercastSocket();
    supercast_socket->moveToThread(&socket_thread);
    socket_thread.start();

}


Supercast::~Supercast()
{
    socket_thread.quit();
    socket_thread.wait();
}
