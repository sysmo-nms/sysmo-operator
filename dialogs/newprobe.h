#ifndef NEWPROBE_H
#define NEWPROBE_H

#include "newprobepage1.h"

#include <QWizard>
#include <QWidget>

#include <QDebug>

class NewProbe : public QWizard
{
public:
    NewProbe(QWidget* parent);
    void setTarget(QString target);
private:
    QString current_target;
};

#endif // NEWPROBE_H
