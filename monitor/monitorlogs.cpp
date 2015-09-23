#include "monitorlogs.h"

MonitorLogs* MonitorLogs::singleton = NULL;

MonitorLogs::MonitorLogs(QWidget* parent) : NFrame(parent)
{
    MonitorLogs::singleton = this;
    this->logarea = new QTextEdit(this);
    //this->setFrameShadow(QFrame::StyledPanel);
    NGridContainer* grid = new NGridContainer(this);
    grid->addWidget(this->logarea, 0,0);
}

void MonitorLogs::probeReturn(QJsonObject obj)
{
    this->logarea->append("<b><font color=\"red\">received probe return</font></b>");
}
