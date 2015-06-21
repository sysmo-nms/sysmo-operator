#ifndef NEWPROBEPAGE1_H
#define NEWPROBEPAGE1_H

#include "ngrid.h"
#include "monitor/nchecks.h"

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
#include <QXmlDeclHandler>
#include <QVariant>

#include <QDebug>


class NewProbePage1 : public QWizardPage
{
public:
    /*
     * QWizard parent for connecting to QWizard::next()
     */
    NewProbePage1(QWizard* parent = 0);
    bool isComplete() const;
    int  nextId()     const;

private:
    QTreeView* treeview  = NULL;
    QLineEdit* selection = NULL;
};


class CheckDefParser: public QXmlDefaultHandler
{
public:
    QString name = "";
    QString type = "";
    QString desc = "";
    bool    descIsNext = false;
    bool startElement(
            const QString &namespaceURI,
            const QString &localName,
            const QString &qName,
            const QXmlAttributes &atts);
    bool characters(const QString &ch);

};

#endif // NEWPROBEPAGE1_H
