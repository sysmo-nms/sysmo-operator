#ifndef TARGETTYPEITEM_H
#define TARGETTYPEITEM_H

#include <QStandardItem>
#include <Qt>
#include <QPixmap>
#include <QString>
#include <QVariant>

class TargetTypeItem : public QStandardItem
{
public:
    TargetTypeItem();
    int type() const;
    QVariant data(int role) const;
    QPixmap icon;
    QString text_variable;
};

#endif // TARGETTYPEITEM_H
