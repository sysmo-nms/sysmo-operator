#ifndef NEWPROBE_H
#define NEWPROBE_H

#include "include/dialogs/newprobepage1.h"
#include "include/dialogs/newprobepage2.h"
#include "include/dialogs/newprobepage3.h"

#include <QWizard>
#include <QWidget>

#include <QDebug>

class NewProbe : public QWizard
{
public:
    NewProbe(QString forTarget, QWidget* parent = 0);
};

#endif // NEWPROBE_H
