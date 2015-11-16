#ifndef MONITORACTIONSDIALOG_H
#define MONITORACTIONSDIALOG_H

#include "include/ngrid.h"
#include "include/nframe.h"
#include "include/actions/monitoractioncreate.h"
#include "include/dialogs/messagebox.h"
#include "include/actions/actionprocess.h"

#include <QDialog>
#include <QWidget>
#include <QObject>
#include <QLabel>
#include <QSettings>
#include <QVariant>
#include <QHash>
#include <QDebug>
#include <QPushButton>
#include <QListWidget>
#include <QIcon>
#include <QDialogButtonBox>
#include <QHashIterator>
#include <QListWidgetItem>
#include <QStringList>

class MonitorActionsDialog : public QDialog
{
    Q_OBJECT
public:
    explicit MonitorActionsDialog(QWidget* parent, QString target);

private:
    QString target;
    QListWidget *list_view;
    void updateView();
    QPushButton *editAction;
    QPushButton *delAction;

public slots:
    void handleAddAction();
    void handleDelAction();
    void handleEditAction();

    void handleDoubleClicked(QListWidgetItem *item);
    void handleSelectionChange();
};

#endif // MONITORACTIONSDIALOG_H
