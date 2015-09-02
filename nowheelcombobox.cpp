#include "nowheelcombobox.h"

NoWheelComboBox::NoWheelComboBox(QWidget *parent)
    : QComboBox(parent)
{

}

void NoWheelComboBox::wheelEvent(QWheelEvent *event)
{
    event->ignore();
}
