#ifndef NOWHEELCOMBOBOX_H
#define NOWHEELCOMBOBOX_H

#include <QWidget>
#include <QComboBox>
#include <QWheelEvent>

class NoWheelComboBox : public QComboBox
{
    Q_OBJECT
public:
    explicit NoWheelComboBox(QWidget *parent = 0);
    void wheelEvent(QWheelEvent *event);

signals:

public slots:
};

#endif // NOWHEELCOMBOBOX_H
