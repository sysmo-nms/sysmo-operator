#include "newprobeprogressdialog.h"

NewProbeProgressDialog::NewProbeProgressDialog(
        QHash<QString,QLineEdit*>* args,
        QString target,
        QString probe_name,
        QString probe_class,
        QString display_name,
        QWidget* parent)
        : QProgressDialog(parent)
{
    this->setModal(true);
    this->setLabelText("Applying probe configuration");
    this->setMinimum(0);
    this->setMaximum(0);

    QPushButton *cancel = new QPushButton(this);
    cancel->setDisabled(true);
    cancel->setText("Cancel");
    this->setCancelButton(cancel);

    QJsonObject props;
    QHashIterator<QString, QLineEdit*> i(*args);
    while (i.hasNext()) {
        i.next();
        props.insert(i.key(), i.value()->text());
    }

    QJsonObject createProbeQuery {
        {"from", "monitor"},
        {"type", "createNchecksQuery"},
        {"value", QJsonObject {
                {"target",     target},
                {"display",    display_name},
                {"identifier", probe_name},
                {"class",      probe_class},
                {"properties", props}}}};

    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig, SIGNAL(serverMessage(QJsonObject)),
                this, SLOT(createProbeReply(QJsonObject)));
    Supercast::sendQuery(createProbeQuery, sig);
}


void NewProbeProgressDialog::createProbeReply(QJsonObject reply)
{
    qDebug() << "reply: " << reply;
    bool status = reply.value("value").toObject().value("status").toBool();
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
                    "Probe failed: " + reply.value("value").toObject().value("reply").toString(),
                    QSystemTrayIcon::Critical,
                    10000);
        this->reject();
    }
}
