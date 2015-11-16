#ifndef NEWPROBEPAGE2_H
#define NEWPROBEPAGE2_H

#include "include/sysmo.h"
#include "include/nframe.h"
#include "include/nframecontainer.h"
#include "include/ngrid.h"
#include "include/ngridcontainer.h"
#include "include/monitor/monitor.h"
#include "include/monitor/nchecks.h"
#include "include/monitor/xml/parsecheckmakedoc.h"
#include "include/monitor/xml/parsecheckmakeform.h"
#include "include/dialogs/newprobeprogressdialog.h"
#include "include/dialogs/messagebox.h"
#include "include/network/supercastsignal.h"
#include "include/network/supercast.h"
#include "include/qjson.h"

#include <QWidget>
#include <QObject>
#include <QFormLayout>
#include <QPushButton>
#include <QStringList>
#include <QList>
#include <QLabel>
#include <QWizard>
#include <QWizardPage>
#include <QXmlInputSource>
#include <QXmlSimpleReader>
#include <QTextEdit>
#include <QProgressDialog>
#include <QTreeWidget>
#include <QTreeWidgetItem>
#include <QAbstractItemView>
#include <QHeaderView>
#include <QDialogButtonBox>
#include <QPushButton>
#include <QList>
#include <QVariant>
#include <QString>

#include <QDebug>



class NewProbePage2 : public QWizardPage
{
    Q_OBJECT
public:
    NewProbePage2(QString forTarget, QWizard* parent = 0);
    void initializePage();
    void cleanupPage();
    bool validatePage();
    bool isComplete() const;
    int nextId() const;

private:
    QString     target;
    QString     probe_class;
    QMap<QString,QLineEdit*>* args;
    QTextEdit*  docs;
    NFrame*     form_frame;
    NGrid*      grid;
    QLineEdit *name_line;
    QList<QLineEdit*>* mandatory_args;
};


class HelperExec: public QObject
{
    Q_OBJECT
public:
    HelperExec(QLineEdit* line, QWidget *parent = 0);
    QString    h_class;
    QString    h_target;
    QWidget*   w_parent;
    QLineEdit* flag_line;

private:
    QProgressDialog* dial;

public slots:
    void execHelper();

private slots:
    void helperReply(QVariant reply);
};


class HelperDialog : public QDialog
{
    Q_OBJECT
public:
    HelperDialog(QVariant helperReply, QWidget* parent = 0);
    QString getValue();

private:
    QString value;
    QString list_separator;
    QMap<QString, QTreeWidgetItem*> root_items;

public slots:
    void refreshTreeState(QTreeWidgetItem* item, int column);
    void resetTreeCheckState();
    void validateSelection();
};

#endif // NEWPROBEPAGE2_H
