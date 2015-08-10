#ifndef MONITORACTIONSDIALOG_H
#define MONITORACTIONSDIALOG_H

#include <QDialog>
#include <QWidget>
#include <QObject>
#include <QLabel>

class MonitorActionsDialog : public QDialog
{
public:
    explicit MonitorActionsDialog(QWidget* parent, QString target);
};

#endif // MONITORACTIONSDIALOG_H
