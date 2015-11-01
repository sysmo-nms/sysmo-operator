#ifndef NEWTARGETPAGE1_H
#define NEWTARGETPAGE1_H

#include "sysmo.h"
#include "nframecontainer.h"
#include "ngridcontainer.h"
#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "monitor/treeview.h"
#include "dialogs/messagebox.h"

#include <QObject>
#include <QWidget>
#include <QWizard>
#include <QDialog>
#include <QList>
#include <QListIterator>
#include <QWizardPage>
#include <QFormLayout>
#include <QLineEdit>
#include <QSpinBox>
#include <QComboBox>
#include <QCheckBox>
#include <QDoubleSpinBox>
#include <QFrame>
#include <QLabel>
#include <QString>
#include <QAbstractButton>
#include <QMessageBox>

#include <QDebug>

class NewTargetPage1 : public QWizardPage
{
    Q_OBJECT

public:
    explicit NewTargetPage1(QWidget* parent = 0);
    ~NewTargetPage1();
    bool isComplete() const;
    bool validatePage();

public slots:
    void createTargetReply(QJsonObject reply);

private:
    QLineEdit* target_host;
    QLineEdit* target_name;
    QSpinBox*  snmp_port;
    QSpinBox*  snmp_timeout;
    QComboBox* snmp_version;
    QLineEdit* snmp_community;
    QComboBox* snmp_seclevel;
    QLineEdit* snmp_usm_user;
    QComboBox* snmp_auth_proto;
    QComboBox* snmp_priv_proto;
    QLineEdit* snmp_auth_key;
    QLineEdit* snmp_priv_key;
    QCheckBox* snmp_enable;

    //QCheckBox* include_icmp_probe;

    //QDoubleSpinBox* longitude  = NULL;
    //QDoubleSpinBox* latitude   = NULL;

    QList<QWidget*>* snmp_widgets;
    QList<QWidget*>* snmp_v2_widgets;
    QList<QWidget*>* snmp_v3_widgets;
    QList<QWidget*>* snmp_v3_auth_widgets;
    QList<QWidget*>* snmp_v3_priv_widgets;

    void disableUnusedWidgets() const;
    int  configType() const;
    static int const NO_SNMP              = 0;
    static int const SNMP_V1              = 1;
    static int const SNMP_V2              = 2;
    static int const SNMP_V3_AUTHPRIV     = 3;
    static int const SNMP_V3_AUTHNOPRIV   = 4;
    static int const SNMP_V3_NOAUTHNOPRIV = 5;
};

#endif // NEWTARGETPAGE1_H
