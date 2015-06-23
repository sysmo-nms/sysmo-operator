#ifndef NEWPROBEPROGRESSDIALOG_H
#define NEWPROBEPROGRESSDIALOG_H

#include <QObject>
#include <QWidget>
#include <QProgressDialog>

class NewProbeProgressDialog : public QProgressDialog
{
    Q_OBJECT
public:
    NewProbeProgressDialog(QWidget* parent = 0);
};

#endif // NEWPROBEPROGRESSDIALOG_H
