#include "treedelegateprogress.h"

TreeDelegateProgress::TreeDelegateProgress(QWidget* parent)
        : QStyledItemDelegate(parent)
{
    this->font = QFont();
    this->font.setWeight(QFont::Bold);
}


void TreeDelegateProgress::ticTimeout()
{
    this->timestamp = QDateTime::currentMSecsSinceEpoch() / 1000;
}


void TreeDelegateProgress::paint(
        QPainter* 					painter,
        const QStyleOptionViewItem  &option,
        const QModelIndex 			&index) const
{
    QVariant item_type(index.data(Sysmo::ROLE_IS_PROGRESS_ITEM));
    if (item_type.toInt() == 0) {
        return QStyledItemDelegate::paint(painter, option, index);
    }

    int step = index.data(Sysmo::ROLE_PROGRESS_STEP).toInt(NULL);
    int next = index.data(Sysmo::ROLE_PROGRESS_NEXT).toInt(NULL);

    int in_next = next - this->timestamp;

    QStyleOptionProgressBar opts;
    opts.rect = option.rect;
    opts.minimum = 0;
    opts.maximum = step;

    if (in_next < step) {
        opts.progress = step - in_next;
        opts.text = QString("Step %1/%2")
            .arg(QString::number(step - in_next))
            .arg(QString::number(step));

    } else {
        opts.progress = step;
        opts.text = QString("Step %1/%2")
            .arg(QString::number(step))
            .arg(QString::number(step));

    }

    opts.textVisible = true;
    //painter->setFont(this->font);
    QApplication::style()->drawControl(QStyle::CE_ProgressBar, &opts, painter);
}
