#ifndef TREEDELEGATEPROGRESS_H
#define TREEDELEGATEPROGRESS_H

#include "treemodel.h"

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
#include <QDebug>

class TreeDelegateProgress : public QStyledItemDelegate
{
    Q_OBJECT

public:
    explicit TreeDelegateProgress(QWidget* parent);
    void paint(
            QPainter* painter,
            const QStyleOptionViewItem &option,
            const QModelIndex &index) const Q_DECL_OVERRIDE;
};

#endif // TREEDELEGATEPROGRESS_H
