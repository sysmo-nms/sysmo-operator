#ifndef PROGRESSITEM_H
#define PROGRESSITEM_H

#include "sysmo.h"

#include <QObject>
#include <QStandardItem>

class ProgressItem : public QStandardItem
{
    //Q_OBJECT

public:
    ProgressItem(int step, int timeout);
    QVariant data(int role) const;
    int type() const;
};

#endif // PROGRESSITEM_H
