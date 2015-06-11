#ifndef NEWTARGETPAGE1_H
#define NEWTARGETPAGE1_H

#include "sysmo.h"
#include "nframecontainer.h"
#include "ngridcontainer.h"

#include <QObject>
#include <QWidget>
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

#include <QDebug>

class NewTargetPage1 : public QWizardPage
{
    Q_OBJECT

public:
    NewTargetPage1(QWidget* parent = 0);
    ~NewTargetPage1();
    bool isComplete() const;
    void disableUnusedWidgets() const;

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
    QCheckBox* include_icmp    = NULL;

    QDoubleSpinBox* longitude  = NULL;
    QDoubleSpinBox* latitude   = NULL;

    QList<QWidget*>* snmp_widgets = NULL;
    QList<QWidget*>* snmp_v2_widgets = NULL;
    QList<QWidget*>* snmp_v3_widgets = NULL;
    QList<QWidget*>* snmp_v3_auth_widgets = NULL;
    QList<QWidget*>* snmp_v3_priv_widgets = NULL;

};

#endif // NEWTARGETPAGE1_H
