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
#ifndef NEWPROBEPROGRESSDIALOG_H
#define NEWPROBEPROGRESSDIALOG_H
#include <widgets/lineedit.h>

#include <QProgressDialog>
#include <QMap>
#include <QString>
#include <QWidget>
#include <QVariant>

class NewProbeProgressDialog : public QProgressDialog {
    Q_OBJECT

public:
    NewProbeProgressDialog(
            QMap<QString, LineEdit*>* args,
            QString target,
            QString probe_name,
            QString probe_class,
            QString display_name,
            QWidget* parent = 0);

public slots:
    void createProbeReply(QVariant reply);
};

#endif // NEWPROBEPROGRESSDIALOG_H
