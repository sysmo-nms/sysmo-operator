#ifndef NFRAMECONTAINER_H
#define NFRAMECONTAINER_H

#include <QWidget>
#include <QFrame>

class NFrameContainer : public QFrame
{
    Q_OBJECT
public:
    NFrameContainer(QWidget *parent = 0);
};

#endif // NFRAMECONTAINER_H
