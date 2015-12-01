/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

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
#ifndef LOGIN_H
#define LOGIN_H

#include "include/nframecontainer.h"

#include <QObject>
#include <QWidget>
#include <QDialog>
#include <QLineEdit>
#include <QSpinBox>
#include <QFrame>
#include <QGridLayout>
#include <QFormLayout>
#include <QPushButton>
#include <QLabel>
#include <QDialogButtonBox>
#include <QPixmap>
#include <QRect>
#include <QApplication>
#include <QDesktopWidget>
#include <QSettings>
#include <QVariant>
#include <QHash>
#include <QDebug>

class LogIn : public QDialog
{
    Q_OBJECT

public:
    explicit LogIn(QWidget* parent = 0);
    QString getUserName();
    QString getPassword();
    QString getServerName();
    qint16  getServerPort();
    void saveLoginState();

private:
    QLineEdit*	 user_name;
    QLineEdit*	 user_pass;
    QLineEdit*	 server_name;
    QSpinBox*    server_port;
    QPushButton* ok_but;
    void restoreForm();

    QString default_name;
    QString default_server;
    int default_port;

private slots:
    void isValid();

signals:
    void tryValidate();
};

#endif // LOGIN_H
