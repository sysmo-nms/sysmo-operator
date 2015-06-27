#ifndef PROBEWINDOW_H
#define PROBEWINDOW_H

#include "nframecontainer.h"
#include "ngrid.h"

#include <QObject>
#include <QWidget>
#include <QLabel>

#include <QDebug>

class ProbeWindow : public NFrameContainer
{
    Q_OBJECT
public:
    explicit ProbeWindow(
            QString probeName,
            QWidget *parent = 0);

signals:

public slots:
};

#endif // PROBEWINDOW_H
