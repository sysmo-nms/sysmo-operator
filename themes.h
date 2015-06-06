#ifndef THEMES_H
#define THEMES_H

#include <QPalette>
#include <QColor>

class Themes
{
public:
    static QPalette midnight;
    static QPalette inland;
    static QPalette greys;
    static QPalette snowy;

private:
    static QPalette initMidnight();
    static QPalette initInland();
    static QPalette initGreys();
    static QPalette initSnowy();
};

#endif // THEMES_H
