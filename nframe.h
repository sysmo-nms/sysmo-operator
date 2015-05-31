#ifndef NFRAME_H
#define NFRAME_H

#include <QWidget>
#include <QFrame>
#include <QObject>

class NFrame: public QFrame
{
    Q_OBJECT

public:
    NFrame(QWidget *parent = 0);
};

#endif // NFRAME_H
