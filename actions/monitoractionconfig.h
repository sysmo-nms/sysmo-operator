#ifndef MONITORACTIONCONFIG_H
#define MONITORACTIONCONFIG_H

#include "ngrid.h"
#include "nframe.h"
#include "ngridcontainer.h"

#include <QDialog>
#include <QString>
#include <QTreeWidget>
#include <QTreeWidgetItem>
#include <QStringList>
#include <QLabel>
#include <QDialogButtonBox>
#include <QPushButton>

class MonitorActionConfig : public QDialog
{
    Q_OBJECT

private:
    QString target;
    QTreeWidget *tree_widget;

public:
    explicit MonitorActionConfig(QWidget* parent, QString target);
};

#endif // MONITORACTIONCONFIG_H
