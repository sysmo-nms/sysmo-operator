#ifndef THEMES_H
#define THEMES_H

#include <QApplication>
#include <QPalette>
#include <QColor>

class Themes
{
public:
    static QPalette midnight;
    static QPalette inland;
    static QPalette greys;
    static QPalette snowy;
    static QPalette native;

private:
    static QPalette initMidnight();
    static QPalette initInland();
    static QPalette initGreys();
    static QPalette initSnowy();
    static QPalette initNative();
};

#endif // THEMES_H
