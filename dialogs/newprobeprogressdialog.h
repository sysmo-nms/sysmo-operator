#ifndef NEWPROBEPROGRESSDIALOG_H
#define NEWPROBEPROGRESSDIALOG_H

#include "dialogs/messagebox.h"
#include "network/supercast.h"
#include "network/supercastsignal.h"
#include "systemtray.h"

#include <QObject>
#include <QWidget>
#include <QProgressDialog>
#include <QHash>
#include <QHashIterator>
#include <QLineEdit>
#include <QPushButton>

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
