#ifndef CENTRALWIDGET_H
#define CENTRALWIDGET_H

#include "ngrid.h"
#include "nframe.h"

#include <QWidget>
#include <QGridLayout>
#include <QLabel>

class CentralWidget : public NFrame
{
public:
    CentralWidget(QWidget *parent = 0);
};

#endif // CENTRALWIDGET_H
