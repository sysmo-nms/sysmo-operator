#ifndef NEWPROBEPAGE1_H
#define NEWPROBEPAGE1_H

#include "ngrid.h"
#include "monitor/nchecks.h"
#include "monitor/xml/parsecheckgetinfos.h"
#include "monitor/monitor.h"

#include <Qt>
#include <QObject>
#include <QWidget>
#include <QWizard>
#include <QWizardPage>
#include <QLineEdit>
#include <QPushButton>
#include <QTreeView>
#include <QAbstractItemView>
#include <QStandardItemModel>
#include <QStandardItem>
#include <QSortFilterProxyModel>
#include <QModelIndex>
#include <QList>
#include <QStringList>
#include <QXmlInputSource>
#include <QXmlSimpleReader>
#include <QVariant>
#include <QJsonObject>

#include <QDebug>


class NewProbePage1 : public QWizardPage
{
public:
    /*
     * QWizard parent for connecting to QWizard::next()
     */
    NewProbePage1(QString forTarget, QWizard* parent = 0);
    bool isComplete() const;
    int  nextId()     const;

private:
    QTreeView* treeview  = NULL;
    QLineEdit* selection = NULL;
};

#endif // NEWPROBEPAGE1_H
