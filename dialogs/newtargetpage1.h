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
#include <QJsonObject>
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
    QLineEdit* target_host     = NULL;
    QLineEdit* target_name     = NULL;
    QSpinBox*  snmp_port       = NULL;
    QSpinBox*  snmp_timeout    = NULL;
    QComboBox* snmp_version    = NULL;
    QLineEdit* snmp_community  = NULL;
    QComboBox* snmp_seclevel   = NULL;
    QLineEdit* snmp_usm_user   = NULL;
    QComboBox* snmp_auth_proto = NULL;
    QComboBox* snmp_priv_proto = NULL;
    QLineEdit* snmp_auth_key   = NULL;
    QLineEdit* snmp_priv_key   = NULL;
    QCheckBox* snmp_enable     = NULL;
    QCheckBox* include_icmp_probe = NULL;
    QCheckBox* include_snmp_probe = NULL;

    QDoubleSpinBox* longitude  = NULL;
    QDoubleSpinBox* latitude   = NULL;

    QList<QWidget*>* snmp_widgets         = NULL;
    QList<QWidget*>* snmp_v2_widgets      = NULL;
    QList<QWidget*>* snmp_v3_widgets      = NULL;
    QList<QWidget*>* snmp_v3_auth_widgets = NULL;
    QList<QWidget*>* snmp_v3_priv_widgets = NULL;

    void disableUnusedWidgets() const;
    int  configType() const;
    int const NO_SNMP              = 0;
    int const SNMP_V1              = 1;
    int const SNMP_V2              = 2;
    int const SNMP_V3_AUTHPRIV     = 3;
    int const SNMP_V3_AUTHNOPRIV   = 4;
    int const SNMP_V3_NOAUTHNOPRIV = 5;
};

#endif // NEWTARGETPAGE1_H
