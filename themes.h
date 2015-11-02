#ifndef THEMES_H
#define THEMES_H

#include <QApplication>
#include <QPalette>
#include <QFont>
#include <QColor>

class Themes
{
public:
    static QPalette midnight;
    static QPalette inland;
    static QPalette greys;
    static QPalette iced;

private:
    static QPalette initMidnight();
    static QPalette initInland();
    static QPalette initGreys();
    static QPalette initIced();
};

#endif // THEMES_H
