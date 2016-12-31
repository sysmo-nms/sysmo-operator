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
#include "delegateprobeprogress.h"


DelegateProbeProgress::DelegateProbeProgress(QWidget* parent)
        : QStyledItemDelegate(parent)
{
}


void DelegateProbeProgress::ticTimeout()
{

    this->timestamp = QDateTime::currentDateTime().toTime_t();

}


void DelegateProbeProgress::paint(
        QPainter* 					painter,
        const QStyleOptionViewItem  &option,
        const QModelIndex 			&index) const
{

    QVariant item_type(index.data(Sysmo::ROLE_IS_PROGRESS_ITEM));

    if (item_type.toInt() == 0)
        return QStyledItemDelegate::paint(painter, option, index);

    int step = index.data(Sysmo::ROLE_PROGRESS_STEP).toInt(NULL);
    int next = index.data(Sysmo::ROLE_PROGRESS_NEXT).toInt(NULL);

    int in_next = next - this->timestamp;

    QStyleOptionProgressBar opts;
    opts.rect = option.rect;
    opts.minimum = 0;
    opts.maximum = step;

    if (in_next <= 0)
    {
        opts.text = QString("Processing...");
        opts.progress = step;
    }
    else if (in_next <= step)
    {
        opts.progress = step - in_next;
        opts.text = QString("Step %1/%2")
            .arg(QString::number(step - in_next))
            .arg(QString::number(step));

    }
    else
    {
        opts.progress = step;
        opts.text = QString("Step %1/%2")
            .arg(QString::number(step))
            .arg(QString::number(step));
    }

    opts.textVisible = true;
    QApplication::style()->drawControl(QStyle::CE_ProgressBar, &opts, painter);

}
