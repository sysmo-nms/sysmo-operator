#include "sidebutton.h"


SideButton::SideButton(QWidget *parent)
        : QPushButton(parent)
{
    QSizePolicy size_pol = QSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
    this->setSizePolicy(size_pol);
}
