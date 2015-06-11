#include "newtargetpage1.h"

NewTargetPage1::NewTargetPage1(QWidget* parent) : QWizardPage(parent)
{
    this->setTitle("Add new targets");
    this->setSubTitle("Use this form to add new targets to the system.");
    this->setCommitPage(true);
    QFormLayout* form = new QFormLayout();
    form->setContentsMargins(20,15,20,15);
    this->setLayout(form);

    /*
     * List used to modify the various widgets "enabled" states
     */
    this->snmp_widgets         = new QList<QWidget*>();
    this->snmp_v2_widgets      = new QList<QWidget*>();
    this->snmp_v3_widgets      = new QList<QWidget*>();
    this->snmp_v3_auth_widgets = new QList<QWidget*>();
    this->snmp_v3_priv_widgets = new QList<QWidget*>();


    QLabel* host_lab = new QLabel("Host:", this);
    this->target_host = new QLineEdit(this);
    this->target_host->setPlaceholderText("IP version 4/6 or hostname");
    form->addRow(host_lab, this->target_host);
    QObject::connect(
                this->target_host, SIGNAL(textChanged(QString)),
                this,              SIGNAL(completeChanged()));

    QLabel* name_lab = new QLabel("Display name:", this);
    this->target_name = new QLineEdit(this);
    this->target_name->setPlaceholderText("Is hidden by MIB2::sysName if SNMP is enabled.");
    form->addRow(name_lab, this->target_name);
    QObject::connect(
                this->target_name, SIGNAL(textChanged(QString)),
                this,              SIGNAL(completeChanged()));

    QFrame* separator1 = new QFrame(this);
    separator1->setFixedHeight(10);
    form->addRow(separator1);


    this->snmp_enable = new QCheckBox("Is SNMP enabled", this);
    form->addRow(this->snmp_enable);
    QObject::connect(
                this->snmp_enable, SIGNAL(stateChanged(int)),
                this,              SIGNAL(completeChanged()));

    QLabel* version_lab = new QLabel("Version:", this);
    this->snmp_version = new QComboBox(this);
    this->snmp_version->insertItem(Sysmo::SNMP_VERSION_3, "3");
    this->snmp_version->insertItem(Sysmo::SNMP_VERSION_2, "2c");
    this->snmp_version->insertItem(Sysmo::SNMP_VERSION_1, "1");
    this->snmp_version->setCurrentIndex(Sysmo::SNMP_VERSION_2);
    form->addRow(version_lab, this->snmp_version);
    QObject::connect(
                this->snmp_version, SIGNAL(currentIndexChanged(int)),
                this,               SIGNAL(completeChanged()));
    this->snmp_widgets->append(version_lab);
    this->snmp_widgets->append(this->snmp_version);


    QLabel* port_lab = new QLabel("Port:", this);
    this->snmp_port = new QSpinBox(this);
    this->snmp_port->setMinimum(1);
    this->snmp_port->setMaximum(65535);
    this->snmp_port->setValue(161);
    form->addRow(port_lab, this->snmp_port);
    QObject::connect(
                this->snmp_port, SIGNAL(valueChanged(int)),
                this,            SIGNAL(completeChanged()));
    this->snmp_widgets->append(port_lab);
    this->snmp_widgets->append(this->snmp_port);


    QFrame* separator2 = new QFrame(this);
    separator2->setFixedHeight(5);
    form->addRow(separator2);

    QLabel* community_lab = new QLabel("Community:", this);
    this->snmp_community = new QLineEdit(this);
    this->snmp_community->setText("public");
    this->snmp_community->setPlaceholderText("SNMP v1/v2c community name");
    form->addRow(community_lab, this->snmp_community);
    QObject::connect(
                this->snmp_community, SIGNAL(textChanged(QString)),
                this,                 SIGNAL(completeChanged()));
    this->snmp_widgets->append(community_lab);
    this->snmp_widgets->append(this->snmp_community);
    this->snmp_v2_widgets->append(community_lab);
    this->snmp_v2_widgets->append(this->snmp_community);


    QFrame* separator3 = new QFrame(this);
    separator3->setFixedHeight(5);
    form->addRow(separator3);

    QLabel* seclevel_lab = new QLabel("Security level:", this);
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
    form->addRow(seclevel_lab, this->snmp_seclevel);
    QObject::connect(
                this->snmp_seclevel, SIGNAL(currentIndexChanged(int)),
                this,               SIGNAL(completeChanged()));
    this->snmp_widgets->append(seclevel_lab);
    this->snmp_widgets->append(this->snmp_seclevel);
    this->snmp_v3_widgets->append(seclevel_lab);
    this->snmp_v3_widgets->append(this->snmp_seclevel);


    QLabel* usm_user_lab = new QLabel("User:", this);
    this->snmp_usm_user = new QLineEdit(this);
    this->snmp_usm_user->setPlaceholderText("SNMP v3 user name");
    form->addRow(usm_user_lab, this->snmp_usm_user);
    QObject::connect(
                this->snmp_usm_user, SIGNAL(textChanged(QString)),
                this,                  SIGNAL(completeChanged()));
    this->snmp_widgets->append(usm_user_lab);
    this->snmp_widgets->append(this->snmp_usm_user);
    this->snmp_v3_widgets->append(usm_user_lab);
    this->snmp_v3_widgets->append(this->snmp_usm_user);


    QLabel* auth_lab = new QLabel("Authentication:", this);
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
    form->addRow(auth_lab, auth_frame);
    QObject::connect(
                this->snmp_auth_proto, SIGNAL(currentIndexChanged(int)),
                this,                  SIGNAL(completeChanged()));
    QObject::connect(
                this->snmp_auth_key, SIGNAL(textChanged(QString)),
                this,                  SIGNAL(completeChanged()));
    this->snmp_widgets->append(auth_lab);
    this->snmp_widgets->append(auth_frame);
    this->snmp_v3_widgets->append(auth_lab);
    this->snmp_v3_widgets->append(auth_frame);
    this->snmp_v3_auth_widgets->append(auth_lab);
    this->snmp_v3_auth_widgets->append(auth_frame);

    QLabel* priv_lab = new QLabel("Privacy:", this);
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
    form->addRow(priv_lab, priv_frame);
    QObject::connect(
                this->snmp_priv_proto, SIGNAL(currentIndexChanged(int)),
                this,                  SIGNAL(completeChanged()));
    QObject::connect(
                this->snmp_priv_key, SIGNAL(textChanged(QString)),
                this,                  SIGNAL(completeChanged()));
    this->snmp_widgets->append(priv_lab);
    this->snmp_widgets->append(priv_frame);
    this->snmp_v3_widgets->append(priv_lab);
    this->snmp_v3_widgets->append(priv_frame);
    this->snmp_v3_priv_widgets->append(priv_lab);
    this->snmp_v3_priv_widgets->append(priv_frame);


    QFrame* separator4 = new QFrame(this);
    separator4->setFixedHeight(10);
    form->addRow(separator4);


    this->include_icmp = new QCheckBox("Create ICMP echo presence probe", this);
    this->include_icmp->setChecked(true);
    form->addRow(this->include_icmp);
    QObject::connect(
                this->include_icmp, SIGNAL(stateChanged(int)),
                this,               SIGNAL(completeChanged()));
}


bool NewTargetPage1::isComplete() const
{
    this->disableUnusedWidgets();
    if (this->target_host->text() == "") { return false; }
    if (this->target_name->text() == "") { return false; }
    if (!this->snmp_enable->isChecked()) { return true; }

    if (this->snmp_version->currentIndex() != Sysmo::SNMP_VERSION_3) {
        if (this->snmp_community->text() == "" ) {return false;}
        return true;
    }

    // V3 snmp
    if (this->snmp_usm_user->text() == "") {return false;}
    if (this->snmp_seclevel->currentIndex() ==
            Sysmo::SNMP_SECLEVEL_NO_AUTH_NO_PRIV) {return true;}

    if (this->snmp_auth_key->text() == "") {return false;}
    if (this->snmp_seclevel->currentIndex() ==
            Sysmo::SNMP_SECLEVEL_AUTH_NO_PRIV) {return true;}

    if (this->snmp_priv_key->text() == "") {return false;}
    return true;
}


void NewTargetPage1::disableUnusedWidgets() const
{
    if (!this->snmp_enable->isChecked()) {
        QListIterator<QWidget*> it(*this->snmp_widgets);
        while (it.hasNext()) {
            QWidget* w = it.next();
            w->setDisabled(true);
        }
        return; // END: all snmp widgets disabled (no snmp)
    } else {
        QListIterator<QWidget*> it(*this->snmp_widgets);
        while (it.hasNext()) {
            QWidget* w = it.next();
            w->setDisabled(false);
        }
    }

    if (this->snmp_version->currentIndex() != Sysmo::SNMP_VERSION_3) {
        QListIterator<QWidget*> it(*this->snmp_v3_widgets);
        while (it.hasNext()) {
            QWidget* w = it.next();
            w->setDisabled(true);
        }
        return; // END all snmp v3 widgets disabled (snmp v2)
    } else {
        QListIterator<QWidget*> it(*this->snmp_v2_widgets);
        while (it.hasNext()) {
            QWidget* w = it.next();
            w->setDisabled(true);
        }
    }

    if (this->snmp_seclevel->currentIndex() ==
            Sysmo::SNMP_SECLEVEL_NO_AUTH_NO_PRIV) {
        QListIterator<QWidget*> it1(*this->snmp_v3_auth_widgets);
        while (it1.hasNext()) {
            QWidget* w = it1.next();
            w->setDisabled(true);
        }
        QListIterator<QWidget*> it2(*this->snmp_v3_priv_widgets);
        while (it2.hasNext()) {
            QWidget* w = it2.next();
            w->setDisabled(true);
        }
        return; // END snmp v3 auth and priv widgets disabled (snmp v3 noAuthNoPriv)
    } else if (this->snmp_seclevel->currentIndex() ==
               Sysmo::SNMP_SECLEVEL_AUTH_NO_PRIV) {
        QListIterator<QWidget*> it2(*this->snmp_v3_priv_widgets);
        while (it2.hasNext()) {
            QWidget* w = it2.next();
            w->setDisabled(true);
        }
        return; // END snmp v3 priv widgets disabled (snmp v3 authNoPriv)
    }

    return; // END (snmp v3 authPriv)
}


NewTargetPage1::~NewTargetPage1()
{
    delete this->snmp_widgets;
    delete this->snmp_v2_widgets;
    delete this->snmp_v3_widgets;
    delete this->snmp_v3_auth_widgets;
    delete this->snmp_v3_priv_widgets;
}