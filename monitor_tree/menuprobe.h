#ifndef MENUPROBE_H
#define MENUPROBE_H

#include <QMenu>
#include <QWidget>
#include <QString>
#include <QPoint>
#include <QAction>

#include <QDebug>


class MenuProbe : public QMenu
{
    Q_OBJECT

public:
    MenuProbe(QWidget* parent);
    void showMenuFor(QString target, QPoint at);

};

#endif // MENUPROBE_H
