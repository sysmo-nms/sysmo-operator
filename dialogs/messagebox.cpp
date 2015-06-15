#include "messagebox.h"

MessageBox::MessageBox(QWidget* parent) : QMessageBox(parent)
{

}



void MessageBox::setIconType(int icon_type)
{
    if (icon_type == Sysmo::MESSAGE_ERROR) {
        this->setIconPixmap(QPixmap(":/box_icons/dialog-error.png"));
        return;
    }

    if (icon_type == Sysmo::MESSAGE_WARNING) {
        this->setIconPixmap(QPixmap(":/box_icons/dialog-warning.png"));
        return;
    }

    if (icon_type == Sysmo::MESSAGE_INFO) {
        this->setIconPixmap(QPixmap(":/box_icons/dialog-information.png"));
        return;
    }
}
