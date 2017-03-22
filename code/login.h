/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

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
#include <widgets/lineedit.h>
#include <QDialog>
#include <QString>
#include <QWidget>
#include <QSpinBox>
#include <QPushButton>

class LogIn : public QDialog {
    Q_OBJECT

public:
    explicit LogIn(QWidget* parent = 0);
    QString getUserName();
    QString getPassword();
    QString getServerName();
    qint16 getServerPort();
    void saveLoginState();

private:
    LineEdit* user_name;
    LineEdit* user_pass;
    LineEdit* server_name;
    QSpinBox* server_port;
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
