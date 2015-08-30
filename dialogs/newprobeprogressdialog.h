#ifndef NEWPROBEPROGRESSDIALOG_H
#define NEWPROBEPROGRESSDIALOG_H

#include "network/supercast.h"
#include "network/supercastsignal.h"

#include <QObject>
#include <QWidget>
#include <QProgressDialog>
#include <QJsonObject>
#include <QHash>
#include <QHashIterator>
#include <QLineEdit>

#include <QDebug>

class NewProbeProgressDialog : public QProgressDialog
{
    Q_OBJECT
public:
    NewProbeProgressDialog(
            QHash<QString, QLineEdit*>* args,
            QString target,
            QString probe_name,
            QString probe_class,
            QString display_name,
            QWidget* parent = 0);

public slots:
    void createProbeReply(QJsonObject reply);
};

#endif // NEWPROBEPROGRESSDIALOG_H
