#ifndef SUPERCASTHTTP_H
#define SUPERCASTHTTP_H

#include <QObject>
#include <QWidget>

class SupercastHTTP : public QObject
{
    Q_OBJECT

public:
    explicit SupercastHTTP(QWidget* parent = 0);
};

#endif // SUPERCASTHTTP_H
