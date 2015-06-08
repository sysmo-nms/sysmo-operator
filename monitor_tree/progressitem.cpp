#include "progressitem.h"

ProgressItem::ProgressItem(int step, int timeout) : QStandardItem()
{

}

QVariant ProgressItem::data(int role) const
{
    if (role == Sysmo::ROLE_IS_PROGRESS_ITEM) {return 1;}
    return QStandardItem::data(role);
}

int ProgressItem::type() const
{
    return Sysmo::TYPE_PROBE_PROGRESS;
}
