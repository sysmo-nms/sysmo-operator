#include "statusbuttonwidget.h"

StatusButtonWidget::StatusButtonWidget(QWidget* parent) :
    NFrameContainer(parent)
{
    QTimer* timer = new QTimer(this);
    timer->setInterval(600);
    timer->setSingleShot(false);

    QObject::connect(
                Monitor::getInstance(), SIGNAL(deleteProbe(QVariant)),
                this, SLOT(handleDeleteProbe(QVariant)));
    QObject::connect(
                Monitor::getInstance(), SIGNAL(infoProbe(QVariant)),
                this, SLOT(handleInfoProbe(QVariant)));

    this->status_map = new QMap<QString,QString>();

    NGridContainer* grid = new NGridContainer();
    this->setLayout(grid);

    this->ok = new StatusButton(this, "OK",
                                              QPixmap(":/icons/weather-clear"));
    this->err = new StatusButton(this, "ERROR",
                                   QPixmap(":/icons/weather-few-clouds-night"));
    this->warn = new StatusButton(this, "WARNING",
                                            QPixmap(":/icons/weather-showers"));
    this->crit = new StatusButton(this, "CRITICAL",
                                       QPixmap(":/icons/weather-severe-alert"));
    QObject::connect(
                timer, SIGNAL(timeout()),
                this->err, SLOT(toggleRed()));
    QObject::connect(
                timer, SIGNAL(timeout()),
                this->warn, SLOT(toggleRed()));
     QObject::connect(
                timer, SIGNAL(timeout()),
                this->crit, SLOT(toggleRed()));
     timer->start();

    grid->addWidget(this->crit, 0,0);
    grid->addWidget(this->warn, 1,0);
    grid->addWidget(this->err,  2,0);
    grid->addWidget(this->ok,   3,0);
    this->setFixedWidth(110);
}


void StatusButtonWidget::handleDeleteProbe(QVariant obj_var)
{
    QMap<QString,QVariant> obj = obj_var.toMap();
    QString name = obj.value("name").toString();
    if (this->status_map->contains(name)) {
        QString status = this->status_map->take(name);
        this->decrementStatus(status);
    }
}

void StatusButtonWidget::handleInfoProbe(QVariant obj_var)
{
    QMap<QString,QVariant> obj = obj_var.toMap();
    QString name = obj.value("name").toString();
    QString status = obj.value("status").toString();

    if (!this->status_map->contains(name)) {
        this->incrementStatus(status);
    } else {
        QString old_status = this->status_map->take(name);
        this->decrementStatus(old_status);
        this->incrementStatus(status);

    }
    this->status_map->insert(name,status);
}

void StatusButtonWidget::incrementStatus(QString status)
{
    if (status == "OK") {
            this->ok->increment();
    } else if (status == "ERROR") {
            this->err->increment();
    } else if (status == "WARNING") {
            this->warn->increment();
    } else if (status == "CRITICAL") {
            this->crit->increment();
    }
}

void StatusButtonWidget::decrementStatus(QString status)
{
    if (status == "OK") {
            this->ok->decrement();
    } else if (status == "ERROR") {
            this->err->decrement();
    } else if (status == "WARNING") {
            this->warn->decrement();
    } else if (status == "CRITICAL") {
            this->crit->decrement();
    }
}
