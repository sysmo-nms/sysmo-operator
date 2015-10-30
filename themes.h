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
    static QPalette native;
    static QFont defaultFont;

private:
    static QPalette initMidnight();
    static QPalette initInland();
    static QPalette initGreys();
    static QPalette initIced();
    static QPalette initNative();
    static QFont initFont();
};

#endif // THEMES_H
