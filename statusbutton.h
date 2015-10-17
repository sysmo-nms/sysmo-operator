#ifndef STATUSBUTTON_H
#define STATUSBUTTON_H

#include "ngridcontainer.h"
#include "ngrid.h"

#include <QObject>
#include <QWidget>
#include <QLCDNumber>
#include <QPushButton>
#include <QPixmap>
#include <QLabel>
#include <QFrame>
#include <QPalette>

class StatusButton : public QPushButton
{
public:
    StatusButton(QWidget* parent, QString type, QPixmap pixmap);

private:
    QLCDNumber*  lcd;
};

#endif // STATUSBUTTON_H
