#ifndef NGRIDCONTAINER_H
#define NGRIDCONTAINER_H

#include <QWidget>
#include <QGridLayout>

class NGridContainer : public QGridLayout
{

public:
    explicit NGridContainer(QWidget* parent = 0);
};

#endif // NGRIDCONTAINER_H
