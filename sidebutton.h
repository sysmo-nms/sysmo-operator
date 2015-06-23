#ifndef SIDEBUTTON_H
#define SIDEBUTTON_H

#include <QObject>
#include <QWidget>
#include <QPushButton>
#include <QSizePolicy>
#include <QSize>
#include <QIcon>


class SideButton : public QPushButton
{
    Q_OBJECT

public:
    explicit SideButton(QWidget* parent = 0);
};

#endif // SIDEBUTTON_H
