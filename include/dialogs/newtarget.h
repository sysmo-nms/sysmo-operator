#ifndef NEWTARGET_H
#define NEWTARGET_H

#include "include/sysmo.h"
#include "include/dialogs/newtargetpage1.h"

#include <QObject>
#include <QWidget>
#include <QWizard>

class NewTarget : public QWizard
{
    Q_OBJECT

public:
    explicit NewTarget(QWidget* parent = 0);
};

#endif // NEWTARGET_H