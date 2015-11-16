#ifndef MONITORACTIONCREATE_H
#define MONITORACTIONCREATE_H

#include <include/ngrid.h>
#include <include/nframecontainer.h>
#include <include/ngridcontainer.h>

#include <QObject>
#include <QWidget>
#include <QDialog>
#include <QLineEdit>
#include <QLabel>
#include <QFormLayout>
#include <QPushButton>
#include <QFileDialog>
#include <QDebug>
#include <QStringList>
#include <QDialogButtonBox>
#include <QIcon>
#include <QVariant>
#include <QHash>

class MonitorActionCreate : public QDialog
{
    Q_OBJECT
public:
    explicit MonitorActionCreate(QWidget *parent = 0);
    explicit MonitorActionCreate(
            QString name,QHash<QString, QVariant> conf, QWidget *parent = 0);

    QLineEdit *name;
    QLineEdit *cmd;
    QLineEdit *args;

private:
    QPushButton *apply;
    void initLayout();
signals:

public slots:
    void handleSearchExe();
    void handleEditOk();
};

#endif // MONITORACTIONCREATE_H
