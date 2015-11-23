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
#ifndef DELEGATEPROBEPROGRESS_H
#define DELEGATEPROBEPROGRESS_H

#include "include/monitor/treemodel.h"

#include <QObject>
#include <QWidget>
#include <QStyledItemDelegate>
#include <QPainter>
#include <QModelIndex>
#include <QStyleOptionViewItem>
#include <QStyleOptionProgressBar>
#include <QApplication>
#include <QStyle>
#include <QVariant>
#include <QFont>
#include <QDateTime>

#include <QDebug>

class DelegateProbeProgress : public QStyledItemDelegate
{
    Q_OBJECT

public:
    explicit DelegateProbeProgress(QWidget* parent = 0);
    void paint(
            QPainter* painter,
            const QStyleOptionViewItem &option,
            const QModelIndex &index) const;
public slots:
    void ticTimeout();

private:
    int   timestamp;
    QFont font;

};

#endif // DELEGATEPROBEPROGRESS_H
