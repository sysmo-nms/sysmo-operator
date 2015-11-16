#include "include/dialogs/messagebox.h"

MessageBox::MessageBox(QWidget* parent) : QMessageBox(parent)
{
    /*
    this->setWindowFlags(this->windowFlags() | Qt::WindowStaysOnTopHint);
    QTimer* timer = new QTimer(this);
    timer->setSingleShot(false);
    timer->setInterval(100);
    QObject::connect(
                timer, SIGNAL(timeout()),
                this, SLOT(raise()));
                */
    this->setModal(true);

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
