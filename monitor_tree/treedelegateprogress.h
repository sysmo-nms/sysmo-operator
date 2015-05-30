#ifndef TREEDELEGATEPROGRESS_H
#define TREEDELEGATEPROGRESS_H

#include <QObject>
#include <QWidget>
#include <QStyledItemDelegate>

class TreeDelegateProgress : public QStyledItemDelegate
{
public:
    TreeDelegateProgress(QWidget *parent);
    void paint(
            QPainter *painter,
            const QStyleOptionViewItem &option,
            const QModelIndex &index) const Q_DECL_OVERRIDE;
};

#endif // TREEDELEGATEPROGRESS_H
