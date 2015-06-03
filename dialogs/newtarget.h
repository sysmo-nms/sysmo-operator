#ifndef NEWTARGET_H
#define NEWTARGET_H

#include <QObject>
#include <QWidget>
#include <QWizard>

class NewTarget : public QWizard
{
    Q_OBJECT

public:
    explicit NewTarget(QWidget* parent);
};

#endif // NEWTARGET_H
