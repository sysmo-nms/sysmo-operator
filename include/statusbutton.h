#ifndef STATUSBUTTON_H
#define STATUSBUTTON_H

#include "include/ngridcontainer.h"
#include "include/ngrid.h"

#include <QObject>
#include <QWidget>
#include <QLCDNumber>
#include <QPushButton>
#include <QPixmap>
#include <QLabel>
#include <QFrame>
#include <QPalette>
#include <QDebug>

class StatusButton : public QPushButton
{
    Q_OBJECT
public:
    StatusButton(QWidget* parent, QString type, QPixmap pixmap);
    void increment();
    void decrement();

signals:
    void setText(QString value);

public slots:
    void toggleRed();

private slots:
    void updateText();

private:
    QLCDNumber*  lcd;
    int counter;
    QString type;
    bool red;
};

#endif // STATUSBUTTON_H
