#ifndef NGRID_H
#define NGRID_H

#include <QWidget>
#include <QGridLayout>

class NGrid : public QGridLayout
{

public:
    explicit NGrid(QWidget* parent = 0);
};

#endif // NGRID_H
