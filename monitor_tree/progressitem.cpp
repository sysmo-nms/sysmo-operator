#include "progressitem.h"

ProgressItem::ProgressItem(int step, int timeout) : QStandardItem()
{

}

QVariant ProgressItem::data(int role) const
{
    if (role == Qt::UserRole + 1) {return 1;}
    return QStandardItem::data(role);
}
