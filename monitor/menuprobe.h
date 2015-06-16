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
    MenuProbe(QWidget* parent = 0);
    void showMenuFor(QString target, QPoint at);

private:
    QString probe_name;
};

#endif // MENUPROBE_H
