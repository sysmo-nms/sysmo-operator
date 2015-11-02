#include "statusbutton.h"

StatusButton::StatusButton(QWidget *parent, QString type, QPixmap pixmap)
        : QPushButton(parent)
{
    this->red = false;
    this->type = type;
    this->counter = 0;
    this->setFixedHeight(35);
    this->setToolTip(type);
    this->lcd = new QLCDNumber(this);
    this->lcd->setSegmentStyle(QLCDNumber::Flat);
    this->lcd->setFrameShape(QFrame::StyledPanel);
    //this->lcd->setFrameShadow(QFrame::Plain);
    NGrid* grid = new NGrid();

    QLabel* lab = new QLabel(this);
    lab->setPixmap(pixmap);

    grid->addWidget(lab, 0,0);
    grid->addWidget(this->lcd, 0,1);
    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,1);
    this->setLayout(grid);
    QObject::connect(
                this, SIGNAL(clicked(bool)),
                this, SLOT(updateText()));
    this->lcd->setStyleSheet("");
}

void StatusButton::increment()
{
    this->counter += 1;
    this->lcd->display(this->counter);
}

void StatusButton::decrement()
{
    this->counter -= 1;
    this->lcd->display(this->counter);
    if (this->counter == 0) {
        this->lcd->setStyleSheet("");
    }
}

void StatusButton::updateText()
{
    QString filter = "status:%1";
    emit this->setText(filter.arg(this->type));
}

void StatusButton::toggleRed()
{
    if (this->counter > 0) {
        if (this->red) {
            this->lcd->setStyleSheet("");
            this->red = false;
        } else {
            this->lcd->setStyleSheet("QFrame {border: 2px solid #ef2929;}");
            this->red = true;
        }
    }
}
