/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
 */
#include "newtargetpage1.h"


#include "messagebox.h"
#include "sysmo.h"
#include "nframecontainer.h"
#include "ngridcontainer.h"
#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "monitor/treeview.h"

#include <QObject>
#include <QWizard>
#include <QDialog>
#include <QListIterator>
#include <QFormLayout>
#include <QDoubleSpinBox>
#include <QFrame>
#include <QLabel>
#include <QString>
#include <QAbstractButton>
#include <QMessageBox>
#include <QMap>

#include <QDebug>

NewTargetPage1::NewTargetPage1(QWidget* parent) : QWizardPage(parent) {

    this->setTitle("Add new targets");
    this->setSubTitle("Use this form to add new targets to the system.");
    this->setFinalPage(true);
    QFormLayout* form = new QFormLayout();
    form->setContentsMargins(20, 15, 20, 15);
    this->setLayout(form);

    /*
     * List used to modify the various widgets "enabled" states
     */
    this->snmp_widgets = new QList<QWidget*>();
    this->snmp_v2_widgets = new QList<QWidget*>();
    this->snmp_v3_widgets = new QList<QWidget*>();
    this->snmp_v3_auth_widgets = new QList<QWidget*>();
    this->snmp_v3_priv_widgets = new QList<QWidget*>();


    QLabel* host_lab = new QLabel("Host:", this);
    this->target_host = new LineEdit(this);
    this->target_host->setPlaceholderText("IP version 4/6 or hostname");
    form->addRow(host_lab, this->target_host);
    QObject::connect(
            this->target_host, SIGNAL(textChanged(QString)),
            this, SIGNAL(completeChanged()));

    QLabel* name_lab = new QLabel("Display name:", this);
    this->target_name = new LineEdit(this);
    this->target_name->setPlaceholderText("Optional. Hidden by MIB2::sysName if SNMP is enabled.");
    form->addRow(name_lab, this->target_name);
    QObject::connect(
            this->target_name, SIGNAL(textChanged(QString)),
            this, SIGNAL(completeChanged()));

    /* TODO
    this->include_icmp_probe = new QCheckBox("Create ICMP echo presence probe", this);
    this->include_icmp_probe->setChecked(true);
    form->addRow("", this->include_icmp_probe);

    QObject::connect(
                this->include_icmp_probe, SIGNAL(stateChanged(int)),
                this,                     SIGNAL(completeChanged()));
     */


    QFrame* separator1 = new QFrame(this);
    separator1->setFixedHeight(10);
    form->addRow(separator1);


    this->snmp_enable = new QCheckBox("Is SNMP enabled", this);
    form->addRow(this->snmp_enable);
    QObject::connect(
            this->snmp_enable, SIGNAL(stateChanged(int)),
            this, SIGNAL(completeChanged()));

    QLabel* version_lab = new QLabel("Version:", this);
    this->snmp_version = new QComboBox(this);
    this->snmp_version->insertItem(Sysmo::SNMP_VERSION_3, "3");
    this->snmp_version->insertItem(Sysmo::SNMP_VERSION_2, "2c");
    this->snmp_version->insertItem(Sysmo::SNMP_VERSION_1, "1");
    this->snmp_version->setCurrentIndex(Sysmo::SNMP_VERSION_2);
    form->addRow(version_lab, this->snmp_version);
    QObject::connect(
            this->snmp_version, SIGNAL(currentIndexChanged(int)),
            this, SIGNAL(completeChanged()));
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
            this, SIGNAL(completeChanged()));
    this->snmp_widgets->append(port_lab);
    this->snmp_widgets->append(this->snmp_port);


    QFrame* separator2 = new QFrame(this);
    separator2->setFixedHeight(5);
    form->addRow(separator2);

    QLabel* community_lab = new QLabel("Community:", this);
    this->snmp_community = new LineEdit(this);
    this->snmp_community->setText("public");
    this->snmp_community->setPlaceholderText("SNMP v1/v2c community name");
    form->addRow(community_lab, this->snmp_community);
    QObject::connect(
            this->snmp_community, SIGNAL(textChanged(QString)),
            this, SIGNAL(completeChanged()));
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
            this, SIGNAL(completeChanged()));
    this->snmp_widgets->append(seclevel_lab);
    this->snmp_widgets->append(this->snmp_seclevel);
    this->snmp_v3_widgets->append(seclevel_lab);
    this->snmp_v3_widgets->append(this->snmp_seclevel);


    QLabel* usm_user_lab = new QLabel("User:", this);
    this->snmp_usm_user = new LineEdit(this);
    this->snmp_usm_user->setPlaceholderText("SNMP v3 user name");
    form->addRow(usm_user_lab, this->snmp_usm_user);
    QObject::connect(
            this->snmp_usm_user, SIGNAL(textChanged(QString)),
            this, SIGNAL(completeChanged()));
    this->snmp_widgets->append(usm_user_lab);
    this->snmp_widgets->append(this->snmp_usm_user);
    this->snmp_v3_widgets->append(usm_user_lab);
    this->snmp_v3_widgets->append(this->snmp_usm_user);


    QLabel* auth_lab = new QLabel("Authentication:", this);
    NFrameContainer* auth_frame = new NFrameContainer(this);
    NGridContainer* auth_grid = new NGridContainer();
    auth_frame->setLayout(auth_grid);
    this->snmp_auth_proto = new QComboBox(this);
    this->snmp_auth_proto->setFixedWidth(100);
    this->snmp_auth_proto->insertItem(Sysmo::SNMP_AUTH_SHA, "SHA");
    this->snmp_auth_proto->insertItem(Sysmo::SNMP_AUTH_MD5, "MD5");
    this->snmp_auth_proto->setCurrentIndex(Sysmo::SNMP_AUTH_MD5);
    this->snmp_auth_key = new LineEdit(this);
    this->snmp_auth_key->setPlaceholderText("SNMP v3 authentication key");
    auth_grid->addWidget(this->snmp_auth_proto, 0, 0);
    auth_grid->addWidget(this->snmp_auth_key, 0, 1);
    form->addRow(auth_lab, auth_frame);
    QObject::connect(
            this->snmp_auth_proto, SIGNAL(currentIndexChanged(int)),
            this, SIGNAL(completeChanged()));
    QObject::connect(
            this->snmp_auth_key, SIGNAL(textChanged(QString)),
            this, SIGNAL(completeChanged()));
    this->snmp_widgets->append(auth_lab);
    this->snmp_widgets->append(auth_frame);
    this->snmp_v3_widgets->append(auth_lab);
    this->snmp_v3_widgets->append(auth_frame);
    this->snmp_v3_auth_widgets->append(auth_lab);
    this->snmp_v3_auth_widgets->append(auth_frame);

    QLabel* priv_lab = new QLabel("Privacy:", this);
    NFrameContainer* priv_frame = new NFrameContainer(this);
    NGridContainer* priv_grid = new NGridContainer();
    priv_frame->setLayout(priv_grid);
    this->snmp_priv_proto = new QComboBox(this);
    this->snmp_priv_proto->setFixedWidth(100);
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_AES128, "AES");
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_DES, "DES");
    this->snmp_priv_proto->insertSeparator(15);
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_AES192, "AES 192");
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_AES256, "AES 256");
    this->snmp_priv_proto->insertItem(Sysmo::SNMP_PRIV_3DES, "3DES");
    this->snmp_priv_proto->setCurrentIndex(Sysmo::SNMP_PRIV_AES128);
    this->snmp_priv_key = new LineEdit(this);
    this->snmp_priv_key->setPlaceholderText("SNMP v3 privacy key");
    priv_grid->addWidget(this->snmp_priv_proto, 0, 0);
    priv_grid->addWidget(this->snmp_priv_key, 0, 1);
    form->addRow(priv_lab, priv_frame);
    QObject::connect(
            this->snmp_priv_proto, SIGNAL(currentIndexChanged(int)),
            this, SIGNAL(completeChanged()));
    QObject::connect(
            this->snmp_priv_key, SIGNAL(textChanged(QString)),
            this, SIGNAL(completeChanged()));
    this->snmp_widgets->append(priv_lab);
    this->snmp_widgets->append(priv_frame);
    this->snmp_v3_widgets->append(priv_lab);
    this->snmp_v3_widgets->append(priv_frame);
    this->snmp_v3_priv_widgets->append(priv_lab);
    this->snmp_v3_priv_widgets->append(priv_frame);

}

NewTargetPage1::~NewTargetPage1() {

    delete this->snmp_widgets;
    delete this->snmp_v2_widgets;
    delete this->snmp_v3_widgets;
    delete this->snmp_v3_auth_widgets;
    delete this->snmp_v3_priv_widgets;

}

bool NewTargetPage1::isComplete() const {

    this->disableUnusedWidgets();
    if (this->target_host->text() == "") return false;
    if (!this->snmp_enable->isChecked()) return true;

    if (this->snmp_version->currentIndex() != Sysmo::SNMP_VERSION_3) {
        if (this->snmp_community->text() == "") return false;
        return true;
    }

    // V3 snmp
    if (this->snmp_usm_user->text() == "") return false;
    if (this->snmp_seclevel->currentIndex() ==
            Sysmo::SNMP_SECLEVEL_NO_AUTH_NO_PRIV) return true;

    if (this->snmp_auth_key->text() == "") return false;
    if (this->snmp_seclevel->currentIndex() ==
            Sysmo::SNMP_SECLEVEL_AUTH_NO_PRIV) return true;

    if (this->snmp_priv_key->text() == "") return false;
    return true;

}

void NewTargetPage1::disableUnusedWidgets() const {

    if (!this->snmp_enable->isChecked()) {
        QListIterator<QWidget*> it(*this->snmp_widgets);
        while (it.hasNext()) {
            QWidget* w = it.next();
            w->setDisabled(true);
        }
        return; // <---- END: all snmp widgets disabled (no snmp)
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
        return; // <---- END all snmp v3 widgets disabled (snmp v2)
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
        return; // <---- END auth/priv widgets disabled (snmp v3 noAuthNoPriv)
    } else if (this->snmp_seclevel->currentIndex() ==
            Sysmo::SNMP_SECLEVEL_AUTH_NO_PRIV) {
        QListIterator<QWidget*> it2(*this->snmp_v3_priv_widgets);
        while (it2.hasNext()) {
            QWidget* w = it2.next();
            w->setDisabled(true);
        }
        return; // <---- END priv widgets disabled (snmp v3 authNoPriv)
    }

    return; // <---- END (snmp v3 authPriv)

}

int NewTargetPage1::configType() const {

    if (!this->snmp_enable->isChecked())
        return NewTargetPage1::NO_SNMP;

    if (this->snmp_version->currentIndex() == Sysmo::SNMP_VERSION_1)
        return NewTargetPage1::SNMP_V1;
    if (this->snmp_version->currentIndex() == Sysmo::SNMP_VERSION_2)
        return NewTargetPage1::SNMP_V2;

    // then it is v3
    if (this->snmp_seclevel->currentIndex() == Sysmo::SNMP_SECLEVEL_NO_AUTH_NO_PRIV)
        return NewTargetPage1::SNMP_V3_NOAUTHNOPRIV;
    if (this->snmp_seclevel->currentIndex() == Sysmo::SNMP_SECLEVEL_AUTH_NO_PRIV)
        return NewTargetPage1::SNMP_V3_AUTHNOPRIV;

    // then it is v3 authpriv
    return NewTargetPage1::SNMP_V3_AUTHPRIV;

}

bool NewTargetPage1::validatePage() {

    QMap<QString, QVariant> sysProperties;
    if (this->configType() == NewTargetPage1::NO_SNMP) {
        // sysProperties empty

    } else if (this->configType() == NewTargetPage1::SNMP_V1) {
        sysProperties.insert("snmp_port",
                QString::number(this->snmp_port->value()));
        sysProperties.insert("snmp_version",
                "1");
        sysProperties.insert("snmp_community",
                this->snmp_community->text());

    } else if (this->configType() == NewTargetPage1::SNMP_V2) {
        sysProperties.insert("snmp_port",
                QString::number(this->snmp_port->value()));
        sysProperties.insert("snmp_version",
                "2c");
        sysProperties.insert("snmp_community",
                this->snmp_community->text());

    } else if (this->configType() == NewTargetPage1::SNMP_V3_NOAUTHNOPRIV) {
        sysProperties.insert("snmp_port",
                QString::number(this->snmp_port->value()));
        sysProperties.insert("snmp_version",
                "3");
        sysProperties.insert("snmp_seclevel",
                "noAuthNoPriv");
        sysProperties.insert("snmp_usm_user",
                this->snmp_usm_user->text());

    } else if (this->configType() == NewTargetPage1::SNMP_V3_AUTHNOPRIV) {
        QString authproto;
        if (this->snmp_auth_proto->currentIndex() == Sysmo::SNMP_AUTH_MD5) {
            authproto = "MD5";
        } else {
            authproto = "SHA";
        }

        sysProperties.insert("snmp_port",
                QString::number(this->snmp_port->value()));
        sysProperties.insert("snmp_version",
                "3");
        sysProperties.insert("snmp_seclevel",
                "authNoPriv");
        sysProperties.insert("snmp_usm_user",
                this->snmp_usm_user->text());
        sysProperties.insert("snmp_authproto",
                authproto);
        sysProperties.insert("snmp_authkey",
                this->snmp_auth_key->text());


    } else if (this->configType() == NewTargetPage1::SNMP_V3_AUTHPRIV) {
        QString authproto;
        QString privproto;
        if (this->snmp_auth_proto->currentIndex() == Sysmo::SNMP_AUTH_MD5)
            authproto = "MD5";
        else
            authproto = "SHA";

        int privprotoIndex = this->snmp_priv_proto->currentIndex();
        if (privprotoIndex == Sysmo::SNMP_PRIV_3DES)
            privproto = "3DES";
        else if (privprotoIndex == Sysmo::SNMP_PRIV_AES128)
            privproto = "AES";
        else if (privprotoIndex == Sysmo::SNMP_PRIV_AES192)
            privproto = "AES192";
        else if (privprotoIndex == Sysmo::SNMP_PRIV_AES256)
            privproto = "AES256";
        else if (privprotoIndex == Sysmo::SNMP_PRIV_DES)
            privproto = "DES";

        qDebug() << "current index is: " << privprotoIndex;

        sysProperties.insert("snmp_port",
                QString::number(this->snmp_port->value()));
        sysProperties.insert("snmp_version",
                "3");
        sysProperties.insert("snmp_seclevel",
                "authPriv");
        sysProperties.insert("snmp_usm_user",
                this->snmp_usm_user->text());
        sysProperties.insert("snmp_authproto",
                authproto);
        sysProperties.insert("snmp_authkey",
                this->snmp_auth_key->text());
        sysProperties.insert("snmp_privproto",
                privproto);
        sysProperties.insert("snmp_privkey",
                this->snmp_priv_key->text());

    }

    QMap<QString, QVariant> createTargetQuery;
    QMap<QString, QVariant> props;
    props.insert("host", this->target_host->text());
    props.insert("name", this->target_name->text());
    QMap<QString, QVariant> value;
    value.insert("properties", props);
    value.insert("sysProperties", sysProperties);
    createTargetQuery.insert("from", "monitor");
    createTargetQuery.insert("type", "createTargetQuery");
    createTargetQuery.insert("value", value);
    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
            sig, SIGNAL(serverMessage(QVariant)),
            this, SLOT(createTargetReply(QVariant)));
    Supercast::sendQuery(createTargetQuery, sig);
    return false;

}

void NewTargetPage1::createTargetReply(QVariant replyVariant) {

    QMap<QString, QVariant> reply = replyVariant.toMap();
    qDebug() << "received qt reply: " << reply;
    QMap<QString, QVariant> val = reply.value("value").toMap();
    bool status = val.value("status").toBool();

    MessageBox msgbox(this);
    if (status) {

        msgbox.setIconType(Sysmo::MESSAGE_INFO);
        msgbox.setText("Target successfuly created");
        msgbox.setInformativeText("Do you want to create another target?");
        msgbox.setStandardButtons(QMessageBox::Yes | QMessageBox::No);
        msgbox.setDefaultButton(QMessageBox::No);
        int ret = msgbox.exec();
        if (ret == QMessageBox::No) {
            this->wizard()->button(QWizard::CancelButton)->click();
        } else {
            this->target_host->setFocus();
        }
    } else {
        QString error = val.value("reply").toString();
        msgbox.setIconType(Sysmo::MESSAGE_ERROR);
        msgbox.setText(error);
        msgbox.setStandardButtons(QMessageBox::Ok);
        msgbox.exec();
    }

}
