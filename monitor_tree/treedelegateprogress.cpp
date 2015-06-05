#include "treedelegateprogress.h"

TreeDelegateProgress::TreeDelegateProgress(QWidget* parent)
        : QStyledItemDelegate(parent)
{

}


void TreeDelegateProgress::paint(
        QPainter* painter,
        const QStyleOptionViewItem &option,
        const QModelIndex &index) const
{
    QVariant v(index.data(Qt::UserRole + 1));
    if (v.toInt() == 0) {
        QStyledItemDelegate::paint(painter, option, index);
        return;
    }


    painter->save();
    QStyleOptionProgressBar opts;
    opts.text = "Step 150/300";
    opts.rect = option.rect;
    opts.minimum = 0;
    opts.maximum = 100;
    opts.progress = 50;
    opts.textVisible = true;
    opts.textAlignment = Qt::AlignCenter;
    QApplication::style()->drawControl(QStyle::CE_ProgressBar, &opts, painter);
    painter->restore();
}
