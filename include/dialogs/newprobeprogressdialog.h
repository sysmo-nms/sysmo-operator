#ifndef NEWPROBEPROGRESSDIALOG_H
#define NEWPROBEPROGRESSDIALOG_H

#include "include/dialogs/messagebox.h"
#include "include/network/supercast.h"
#include "include/network/supercastsignal.h"
#include "include/systemtray.h"

#include <QObject>
#include <QWidget>
#include <QProgressDialog>
#include <QMap>
#include <QMapIterator>
#include <QLineEdit>
#include <QPushButton>
#include <QVariant>

#include <QDebug>

class NewProbeProgressDialog : public QProgressDialog
{

    Q_OBJECT

public:
    NewProbeProgressDialog(
            QMap<QString, QLineEdit*>* args,
            QString target,
            QString probe_name,
            QString probe_class,
            QString display_name,
            QWidget* parent = 0);

public slots:
    void createProbeReply(QVariant reply);
};

#endif // NEWPROBEPROGRESSDIALOG_H
