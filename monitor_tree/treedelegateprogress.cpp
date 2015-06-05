#include "treedelegateprogress.h"

TreeDelegateProgress::TreeDelegateProgress(QWidget* parent)
        : QStyledItemDelegate(parent)
{
    this->ticval = 0;
    this->font = QFont();
    this->font.setWeight(QFont::Bold);
}


void TreeDelegateProgress::ticTimeout()
{
    qDebug() << "should update tic";
    this->ticval = this->ticval + 1;

}


void TreeDelegateProgress::paint(
        QPainter* 					painter,
        const QStyleOptionViewItem  &option,
        const QModelIndex 			&index) const
{
    QVariant item_type(index.data(Qt::UserRole + 1));
    if (item_type.toInt() == 0) {
        return QStyledItemDelegate::paint(painter, option, index);
    }
    painter->save();
    QStyleOptionProgressBar opts;
    opts.text = QString("Step %1/%2").arg(QString::number(this->ticval)).arg(QString::number(100));
    opts.rect = option.rect;
    opts.minimum = 0;
    opts.maximum = 100;

    if (this->ticval < 101) {
        opts.progress = this->ticval;
    } else {
        opts.progress = 100;
    }

    opts.textVisible = true;
    painter->setFont(this->font);
    QApplication::style()->drawControl(QStyle::CE_ProgressBar, &opts, painter);
    painter->restore();
}
