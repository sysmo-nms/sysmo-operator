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
#include "newprobeprogressdialog.h"

#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "systemtray.h"

#include "messagebox.h"

#include <QObject>
#include <QMapIterator>
#include <QPushButton>

#include <QDebug>

NewProbeProgressDialog::NewProbeProgressDialog(
        QMap<QString, LineEdit*>* args,
        QString target,
        QString probe_name,
        QString probe_class,
        QString display_name,
        QWidget* parent)
: QProgressDialog(parent) {

    this->setModal(true);
    this->setLabelText("Applying probe configuration");
    this->setMinimum(0);
    this->setMaximum(0);

    QPushButton *cancel = new QPushButton(this);
    cancel->setDisabled(true);
    cancel->setText("Cancel");
    this->setCancelButton(cancel);

    QMap<QString, QVariant> props;
    QMapIterator<QString, LineEdit*> i(*args);
    while (i.hasNext()) {
        i.next();
        props.insert(i.key(), i.value()->text());
    }

    QMap<QString, QVariant> createProbeQuery;
    QMap<QString, QVariant> value;
    value.insert("target", target);
    value.insert("display", display_name);
    value.insert("identifier", probe_name);
    value.insert("class", probe_class);
    value.insert("properties", props);
    createProbeQuery.insert("from", "monitor");
    createProbeQuery.insert("type", "createNchecksQuery");
    createProbeQuery.insert("value", value);

    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
            sig, SIGNAL(serverMessage(QVariant)),
            this, SLOT(createProbeReply(QVariant)));
    Supercast::sendQuery(createProbeQuery, sig);

}

void NewProbeProgressDialog::createProbeReply(QVariant replyVariant) {

    QMap<QString, QVariant> reply = replyVariant.toMap();
    qDebug() << "reply: " << reply;
    bool status = reply.value("value").toMap().value("status").toBool();
    if (status) {
        SystemTray::singleton->showMessage(
                "Create probe reply:",
                "Probe successfuly created",
                QSystemTrayIcon::Information,
                2000);
        this->accept();
    } else {
        SystemTray::singleton->showMessage(
                "Create probe reply:",
                "Probe failed: " + reply.value("value").toMap().value("reply").toString(),
                QSystemTrayIcon::Critical,
                10000);
        this->reject();
    }

}
