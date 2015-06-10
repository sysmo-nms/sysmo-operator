#include "newtargetpage1.h"

NewTargetPage1::NewTargetPage1(QWidget* parent) : QWizardPage(parent)
{
    this->setTitle("Add new targets");
    this->setSubTitle("Use this form to add new targets to the system.");
    QFormLayout* form = new QFormLayout();
    form->setContentsMargins(20,15,20,15);
    this->setLayout(form);


    this->target_host = new QLineEdit(this);
    this->target_host->setPlaceholderText("IP version 4/6 or hostname");
    form->addRow("Host:", this->target_host);


    this->target_name = new QLineEdit(this);
    this->target_name->setPlaceholderText("Optional");
    form->addRow("Name:", this->target_name);


    QFrame* separator1 = new QFrame(this);
    separator1->setFixedHeight(10);
    form->addRow(separator1);


    this->snmp_enable = new QCheckBox("SNMP support", this);
    form->addRow(this->snmp_enable);


    this->snmp_port = new QSpinBox(this);
    this->snmp_port->setMinimum(1);
    this->snmp_port->setMaximum(65535);
    this->snmp_port->setValue(161);
    form->addRow("Port:", this->snmp_port);


    // timeout??


    this->snmp_version = new QComboBox(this);
    this->snmp_version->insertItem(Sysmo::SNMP_VERSION_3, "3");
    this->snmp_version->insertItem(Sysmo::SNMP_VERSION_2, "2c");
    this->snmp_version->insertItem(Sysmo::SNMP_VERSION_1, "1");
    this->snmp_version->setCurrentIndex(Sysmo::SNMP_VERSION_2);
    form->addRow("Version:", this->snmp_version);


    this->snmp_community = new QLineEdit(this);
    this->snmp_community->setText("public");
    this->snmp_community->setPlaceholderText("SNMP v1/v2c community name");
    form->addRow("Community:", this->snmp_community);


    this->snmp_seclevel = new QComboBox(this);
    this->snmp_seclevel->insertItem(
                Sysmo::SNMP_SECLEVEL_AUTH_PRIV,
                "authPriv");
    this->snmp_seclevel->insertItem(
                Sysmo::SNMP_SECLEVEL_AUTH_NO_PRIV,
                "authNoPriv");
    this->snmp_seclevel->insertItem(
                Sysmo::SNMP_SECLEVEL_NO_AUTH_NO_PRIV,
                "noAuthNoPriv");

    form->addRow("Security level:", this->snmp_seclevel);


    this->snmp_usm_user = new QLineEdit(this);
    this->snmp_usm_user->setPlaceholderText("SNMP v3 user name");
    form->addRow("User:", this->snmp_usm_user);


    NFrameContainer* auth_frame = new NFrameContainer(this);
    NGridContainer*  auth_grid = new NGridContainer();
    auth_frame->setLayout(auth_grid);
    this->snmp_auth_proto = new QComboBox(this);
    this->snmp_auth_proto->setFixedWidth(100);
    this->snmp_auth_proto->insertItem(Sysmo::SNMP_AUTH_SHA, "SHA");
    this->snmp_auth_proto->insertItem(Sysmo::SNMP_AUTH_MD5, "MD5");
    this->snmp_auth_proto->setCurrentIndex(Sysmo::SNMP_AUTH_MD5);
    this->snmp_auth_key = new QLineEdit(this);
    this->snmp_auth_key->setPlaceholderText("SNMP v3 authentication key");
    auth_grid->addWidget(this->snmp_auth_proto, 0,0);
    auth_grid->addWidget(this->snmp_auth_key,   0,1);
    form->addRow("Authentication:", auth_frame);


    NFrameContainer* priv_frame = new NFrameContainer(this);
    NGridContainer*  priv_grid = new NGridContainer();
    priv_frame->setLayout(priv_grid);
    this->snmp_priv_proto = new QComboBox(this);
    this->snmp_priv_proto->setFixedWidth(100);
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_AES128, "AES");
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_DES,    "DES");
    this->snmp_priv_proto->insertSeparator(15);
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_AES192, "AES 192");
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_AES256, "AES 256");
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_3DES,   "3DES");
    this->snmp_priv_proto->setCurrentIndex(Sysmo::SNMP_PRIV_AES128);
    this->snmp_priv_key = new QLineEdit(this);
    this->snmp_priv_key->setPlaceholderText("SNMP v3 privacy key");
    priv_grid->addWidget(this->snmp_priv_proto, 0,0);
    priv_grid->addWidget(this->snmp_priv_key,   0,1);
    form->addRow("Privacy:", priv_frame);


    QFrame* separator2 = new QFrame(this);
    separator1->setFixedHeight(10);
    form->addRow(separator2);


    this->include_icmp = new QCheckBox("Create ICMP echo presence probe", this);
    this->include_icmp->setChecked(true);
    form->addRow(this->include_icmp);
}

