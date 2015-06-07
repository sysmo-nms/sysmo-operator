#include "targettypeitem.h"

TargetTypeItem::TargetTypeItem() : QStandardItem() { }
int TargetTypeItem::type() const { return 1002; }

QVariant TargetTypeItem::data(int role) const
{
    if (role == Qt::DecorationRole) {return this->icon;}
    if (role == Qt::DisplayRole)    {return this->text_variable;}
    return QStandardItem::data(role);
}
