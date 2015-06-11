#ifndef DELEGATEPROBEPROGRESS_H
#define DELEGATEPROBEPROGRESS_H

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
#include <QFont>
#include <QDateTime>

#include <QDebug>

class DelegateProbeProgress : public QStyledItemDelegate
{
    Q_OBJECT

public:
    explicit DelegateProbeProgress(QWidget* parent);
    void paint(
            QPainter* painter,
            const QStyleOptionViewItem &option,
            const QModelIndex &index) const Q_DECL_OVERRIDE;
public slots:
    void ticTimeout();

private:
    int   timestamp;
    QFont font;

};

#endif // DELEGATEPROBEPROGRESS_H
