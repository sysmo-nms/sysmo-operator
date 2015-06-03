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
    QStyledItemDelegate::paint(painter, option, index);
}
