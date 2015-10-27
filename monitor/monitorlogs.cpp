#include "monitorlogs.h"

MonitorLogs::MonitorLogs(QWidget* parent) : QTabWidget(parent)
{
    this->table = new MonitorTableLogs(this);
    this->table->setColumnCount(5);
    this->table->verticalHeader()->hide();
    QStringList headers;
    headers << "Date" << "Target" << "Probe" << "Status" << "Message";
    this->table->setHorizontalHeaderLabels(headers);
    QHeaderView* head = this->table->horizontalHeader();
    head->setStretchLastSection(true);
    NFrameContainer* f1 = new NFrameContainer(this);
    NGrid* g1 = new NGrid();
    f1->setLayout(g1);
    g1->addWidget(this->table);
    NFrame* f2 = new NFrame(this);

    this->insertTab(0, f1, QIcon(":/icons/edit-paste.png"), "Table logs");
    this->insertTab(1, f2, QIcon(":/icons/appointment-new.png"), "Timeline logs");
    this->setTabEnabled(1, false);
    QObject::connect(
                Monitor::getInstance(), SIGNAL(initialSyncBegin(QJsonObject)),
                this, SLOT(handleInitialSyncBegin(QJsonObject)));
}

void MonitorLogs::handleInitialSyncBegin(QJsonObject message)
{
    QString syncDir = "sync";
    QString dumpDir = message.value("dumpDir").toString();
    QString evtFile = message.value("latestEventsFile").toString();
    QString http_tmp = "/%1/%2/%3";
    QString http_url = http_tmp.arg(syncDir).arg(dumpDir).arg(evtFile);
    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
                sig, SIGNAL(serverMessage(QString)),
                this, SLOT(handleHttpReply(QString)));
    Supercast::httpGet(http_url, sig);
}

void MonitorLogs::handleHttpReply(QString body) {
    QJsonDocument json_doc = QJsonDocument::fromJson(body.toUtf8());
    QJsonArray json_array = json_doc.array();
    this->table->setRowCount(json_array.size());
    QJsonArray::iterator i;
    int j = 0;
    for (i = json_array.begin(); i != json_array.end(); i++) {
       QJsonObject obj = (*i).toObject();
       int timestamp = obj.value("DATE_CREATED").toInt();
       QDateTime date = QDateTime::fromTime_t(timestamp);
       QTableWidgetItem* created = new QTableWidgetItem(date.toString("yyyy-MM-d hh:mm:ss"));
       this->table->setItem(j, 0, created);
       this->table->setRowHeight(j, 20);
       j++;
       qDebug() << obj;
    }
}

MonitorTableLogs::MonitorTableLogs(QWidget *parent) : QTableWidget(parent)
{
}
