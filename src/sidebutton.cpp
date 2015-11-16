#include "include/sidebutton.h"

SideButton::SideButton(QWidget* parent) : QPushButton(parent)
{
    this->setSizePolicy(QSizePolicy(QSizePolicy::Ignored,QSizePolicy::Ignored));
}
