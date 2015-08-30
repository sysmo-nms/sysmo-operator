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
}
