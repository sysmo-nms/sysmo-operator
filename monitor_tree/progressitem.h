#ifndef PROGRESSITEM_H
#define PROGRESSITEM_H

#include <QObject>
#include <QStandardItem>

class ProgressItem : public QStandardItem
{
public:
    ProgressItem(int step, int timeout);
    QVariant data(int role) const;
};

#endif // PROGRESSITEM_H
