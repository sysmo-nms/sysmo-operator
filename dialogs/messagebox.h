#ifndef MESSAGEBOX_H
#define MESSAGEBOX_H

#include "sysmo.h"

#include <QObject>
#include <QWidget>
#include <QMessageBox>
#include <QString>
#include <QPixmap>
#include <QTimer>

class MessageBox : public QMessageBox
{
public:
    explicit MessageBox(QWidget* parent = 0);
    void setIconType(int icon_type);
};

#endif // MESSAGEBOX_H
