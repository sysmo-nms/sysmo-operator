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
#ifndef STATUSBUTTON_H
#define STATUSBUTTON_H
#include <QLCDNumber>
#include <QPushButton>
#include <QWidget>
#include <QPixmap>

class StatusButton : public QPushButton {
    Q_OBJECT
public:
    StatusButton(QWidget* parent, QString type, QPixmap pixmap);
    void increment();
    void decrement();

signals:
    void setText(QString value);

public slots:
    void toggleRed();

private slots:
    void updateText();

private:
    QLCDNumber* lcd;
    int counter;
    QString type;
    bool red;
};

#endif // STATUSBUTTON_H
