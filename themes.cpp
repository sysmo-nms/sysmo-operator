#include "themes.h"

QPalette Themes::midnight = Themes::initMidnight();
QPalette Themes::inland   = Themes::initInland();
QPalette Themes::greys    = Themes::initGreys();
QPalette Themes::iced     = Themes::initIced();
QPalette Themes::native   = Themes::initNative();
QFont Themes::defaultFont = Themes::initFont();

QFont Themes::initFont()
{
    int   fake_argc = 0;
    char* fake_argv[0];
    QApplication fake_app(fake_argc, fake_argv);

    return fake_app.font();
}

QPalette Themes::initNative()
{
    /*
     * Start a fake QApplication to have an initialized
     * system QPalette.
     */
    int   fake_argc = 0;
    char* fake_argv[0];
    QApplication fake_app(fake_argc, fake_argv);

    return fake_app.palette();
}

QPalette Themes::initMidnight()
{
    QPalette p;
    p.setColor(QPalette::Normal,   QPalette::Foreground, QColor(224, 222, 219, 255));
    p.setColor(QPalette::Normal,   QPalette::Button, QColor(64, 63, 62, 255));
    p.setColor(QPalette::Normal,   QPalette::Light, QColor(79, 77, 77, 255));
    p.setColor(QPalette::Normal,   QPalette::Midlight, QColor(65, 64, 64, 255));
    p.setColor(QPalette::Normal,   QPalette::Dark, QColor(23, 22, 22, 255));
    p.setColor(QPalette::Normal,   QPalette::Mid, QColor(41, 40, 40, 255));
    p.setColor(QPalette::Normal,   QPalette::Text, QColor(212, 210, 207, 255));
    p.setColor(QPalette::Normal,   QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::ButtonText, QColor(232, 230, 227, 255));
    p.setColor(QPalette::Normal,   QPalette::Base, QColor(32, 31, 31, 255));
    p.setColor(QPalette::Normal,   QPalette::Window, QColor(48, 47, 47, 255));
    p.setColor(QPalette::Normal,   QPalette::Shadow, QColor(16, 16, 16, 255));
    p.setColor(QPalette::Normal,   QPalette::Highlight, QColor(24, 72, 128, 255));
    p.setColor(QPalette::Normal,   QPalette::HighlightedText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::Link, QColor(80, 142, 216, 255));
    p.setColor(QPalette::Normal,   QPalette::LinkVisited, QColor(142, 121, 165, 255));
    p.setColor(QPalette::Normal,   QPalette::AlternateBase, QColor(36, 35, 35, 255));
    p.setColor(QPalette::Normal,   QPalette::ToolTipBase, QColor(16, 48, 80, 255));
    p.setColor(QPalette::Normal,   QPalette::ToolTipText, QColor(196, 209, 224, 255));
    p.setColor(QPalette::Disabled, QPalette::Foreground, QColor(96, 95, 94, 255));
    p.setColor(QPalette::Disabled, QPalette::Button, QColor(56, 55, 54, 255));
    p.setColor(QPalette::Disabled, QPalette::Light, QColor(75, 73, 73, 255));
    p.setColor(QPalette::Disabled, QPalette::Midlight, QColor(61, 59, 59, 255));
    p.setColor(QPalette::Disabled, QPalette::Dark, QColor(20, 20, 20, 255));
    p.setColor(QPalette::Disabled, QPalette::Mid, QColor(36, 35, 35, 255));
    p.setColor(QPalette::Disabled, QPalette::Text, QColor(83, 82, 81, 255));
    p.setColor(QPalette::Disabled, QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Disabled, QPalette::ButtonText, QColor(108, 106, 105, 255));
    p.setColor(QPalette::Disabled, QPalette::Base, QColor(28, 27, 27, 255));
    p.setColor(QPalette::Disabled, QPalette::Window, QColor(42, 41, 41, 255));
    p.setColor(QPalette::Disabled, QPalette::Shadow, QColor(14, 14, 14, 255));
    p.setColor(QPalette::Disabled, QPalette::Highlight, QColor(42, 41, 41, 255));
    p.setColor(QPalette::Disabled, QPalette::HighlightedText, QColor(96, 95, 94, 255));
    p.setColor(QPalette::Disabled, QPalette::Link, QColor(42, 61, 84, 255));
    p.setColor(QPalette::Disabled, QPalette::LinkVisited, QColor(62, 55, 68, 255));
    p.setColor(QPalette::Disabled, QPalette::AlternateBase, QColor(31, 30, 30, 255));
    p.setColor(QPalette::Disabled, QPalette::ToolTipBase, QColor(16, 48, 80, 255));
    p.setColor(QPalette::Disabled, QPalette::ToolTipText, QColor(196, 209, 224, 255));
    p.setColor(QPalette::Inactive, QPalette::Foreground, QColor(224, 222, 219, 255));
    p.setColor(QPalette::Inactive, QPalette::Button, QColor(64, 63, 62, 255));
    p.setColor(QPalette::Inactive, QPalette::Light, QColor(79, 77, 77, 255));
    p.setColor(QPalette::Inactive, QPalette::Midlight, QColor(65, 64, 64, 255));
    p.setColor(QPalette::Inactive, QPalette::Dark, QColor(23, 22, 22, 255));
    p.setColor(QPalette::Inactive, QPalette::Mid, QColor(41, 40, 40, 255));
    p.setColor(QPalette::Inactive, QPalette::Text, QColor(212, 210, 207, 255));
    p.setColor(QPalette::Inactive, QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Inactive, QPalette::ButtonText, QColor(232, 230, 227, 255));
    p.setColor(QPalette::Inactive, QPalette::Base, QColor(32, 31, 31, 255));
    p.setColor(QPalette::Inactive, QPalette::Window, QColor(48, 47, 47, 255));
    p.setColor(QPalette::Inactive, QPalette::Shadow, QColor(16, 16, 16, 255));
    p.setColor(QPalette::Inactive, QPalette::Highlight, QColor(25, 57, 95, 255));
    p.setColor(QPalette::Inactive, QPalette::HighlightedText, QColor(224, 222, 219, 255));
    p.setColor(QPalette::Inactive, QPalette::Link, QColor(80, 142, 216, 255));
    p.setColor(QPalette::Inactive, QPalette::LinkVisited, QColor(142, 121, 165, 255));
    p.setColor(QPalette::Inactive, QPalette::AlternateBase, QColor(36, 35, 35, 255));
    p.setColor(QPalette::Inactive, QPalette::ToolTipBase, QColor(16, 48, 80, 255));
    p.setColor(QPalette::Inactive, QPalette::ToolTipText, QColor(196, 209, 224, 255));
    return p;
}

QPalette Themes::initInland()
{
    QPalette p;
    p.setColor(QPalette::Normal,   QPalette::Foreground, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Normal,   QPalette::Button, QColor(203, 194, 191, 255));
    p.setColor(QPalette::Normal,   QPalette::Light, QColor(226, 220, 211, 255));
    p.setColor(QPalette::Normal,   QPalette::Midlight, QColor(203, 196, 184, 255));
    p.setColor(QPalette::Normal,   QPalette::Dark, QColor(92, 88, 83, 255));
    p.setColor(QPalette::Normal,   QPalette::Mid, QColor(157, 151, 142, 255));
    p.setColor(QPalette::Normal,   QPalette::Text, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Normal,   QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::ButtonText, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Normal,   QPalette::Base, QColor(244, 234, 231, 255));
    p.setColor(QPalette::Normal,   QPalette::Window, QColor(189, 182, 171, 255));
    p.setColor(QPalette::Normal,   QPalette::Shadow, QColor(57, 55, 52, 255));
    p.setColor(QPalette::Normal,   QPalette::Highlight, QColor(106, 141, 210, 255));
    p.setColor(QPalette::Normal,   QPalette::HighlightedText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::Link, QColor(17, 44, 12, 255));
    p.setColor(QPalette::Normal,   QPalette::LinkVisited, QColor(74, 96, 57, 255));
    p.setColor(QPalette::Normal,   QPalette::AlternateBase, QColor(235, 226, 223, 255));
    p.setColor(QPalette::Normal,   QPalette::ToolTipBase, QColor(164, 162, 139, 255));
    p.setColor(QPalette::Normal,   QPalette::ToolTipText, QColor(19, 24, 17, 255));
    p.setColor(QPalette::Disabled, QPalette::Foreground, QColor(95, 91, 84, 255));
    p.setColor(QPalette::Disabled, QPalette::Button, QColor(190, 182, 177, 255));
    p.setColor(QPalette::Disabled, QPalette::Light, QColor(215, 207, 193, 255));
    p.setColor(QPalette::Disabled, QPalette::Midlight, QColor(192, 185, 172, 255));
    p.setColor(QPalette::Disabled, QPalette::Dark, QColor(86, 83, 77, 255));
    p.setColor(QPalette::Disabled, QPalette::Mid, QColor(148, 143, 133, 255));
    p.setColor(QPalette::Disabled, QPalette::Text, QColor(119, 114, 111, 255));
    p.setColor(QPalette::Disabled, QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Disabled, QPalette::ButtonText, QColor(101, 97, 93, 255));
    p.setColor(QPalette::Disabled, QPalette::Base, QColor(226, 217, 212, 255));
    p.setColor(QPalette::Disabled, QPalette::Window, QColor(178, 171, 159, 255));
    p.setColor(QPalette::Disabled, QPalette::Shadow, QColor(55, 53, 49, 255));
    p.setColor(QPalette::Disabled, QPalette::Highlight, QColor(178, 171, 159, 255));
    p.setColor(QPalette::Disabled, QPalette::HighlightedText, QColor(95, 91, 84, 255));
    p.setColor(QPalette::Disabled, QPalette::Link, QColor(127, 134, 116, 255));
    p.setColor(QPalette::Disabled, QPalette::LinkVisited, QColor(152, 156, 136, 255));
    p.setColor(QPalette::Disabled, QPalette::AlternateBase, QColor(218, 210, 205, 255));
    p.setColor(QPalette::Disabled, QPalette::ToolTipBase, QColor(164, 162, 139, 255));
    p.setColor(QPalette::Disabled, QPalette::ToolTipText, QColor(19, 24, 17, 255));
    p.setColor(QPalette::Inactive, QPalette::Foreground, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::Button, QColor(203, 194, 191, 255));
    p.setColor(QPalette::Inactive, QPalette::Light, QColor(226, 220, 211, 255));
    p.setColor(QPalette::Inactive, QPalette::Midlight, QColor(203, 196, 184, 255));
    p.setColor(QPalette::Inactive, QPalette::Dark, QColor(92, 88, 83, 255));
    p.setColor(QPalette::Inactive, QPalette::Mid, QColor(157, 151, 142, 255));
    p.setColor(QPalette::Inactive, QPalette::Text, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Inactive, QPalette::ButtonText, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::Base, QColor(244, 234, 231, 255));
    p.setColor(QPalette::Inactive, QPalette::Window, QColor(189, 182, 171, 255));
    p.setColor(QPalette::Inactive, QPalette::Shadow, QColor(57, 55, 52, 255));
    p.setColor(QPalette::Inactive, QPalette::Highlight, QColor(151, 169, 210, 255));
    p.setColor(QPalette::Inactive, QPalette::HighlightedText, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::Link, QColor(17, 44, 12, 255));
    p.setColor(QPalette::Inactive, QPalette::LinkVisited, QColor(74, 96, 57, 255));
    p.setColor(QPalette::Inactive, QPalette::AlternateBase, QColor(235, 226, 223, 255));
    p.setColor(QPalette::Inactive, QPalette::ToolTipBase, QColor(164, 162, 139, 255));
    p.setColor(QPalette::Inactive, QPalette::ToolTipText, QColor(19, 24, 17, 255));
    return p;
}

QPalette Themes::initGreys()
{
    QPalette p;
    p.setColor(QPalette::Normal,   QPalette::Foreground, QColor(20, 20, 20, 255));
    p.setColor(QPalette::Normal,   QPalette::Button, QColor(116, 116, 116, 255));
    p.setColor(QPalette::Normal,   QPalette::Light, QColor(159, 159, 159, 255));
    p.setColor(QPalette::Normal,   QPalette::Midlight, QColor(142, 142, 142, 255));
    p.setColor(QPalette::Normal,   QPalette::Dark, QColor(62, 62, 62, 255));
    p.setColor(QPalette::Normal,   QPalette::Mid, QColor(108, 108, 108, 255));
    p.setColor(QPalette::Normal,   QPalette::Text, QColor(40, 40, 40, 255));
    p.setColor(QPalette::Normal,   QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::ButtonText, QColor(10, 10, 10, 255));
    p.setColor(QPalette::Normal,   QPalette::Base, QColor(160, 160, 160, 255));
    p.setColor(QPalette::Normal,   QPalette::Window, QColor(128, 128, 128, 255));
    p.setColor(QPalette::Normal,   QPalette::Shadow, QColor(42, 42, 42, 255));
    p.setColor(QPalette::Normal,   QPalette::Highlight, QColor(82, 98, 118, 255));
    p.setColor(QPalette::Normal,   QPalette::HighlightedText, QColor(180, 180, 180, 255));
    p.setColor(QPalette::Normal,   QPalette::Link, QColor(18, 64, 0, 255));
    p.setColor(QPalette::Normal,   QPalette::LinkVisited, QColor(5, 0, 82, 255));
    p.setColor(QPalette::Normal,   QPalette::AlternateBase, QColor(140, 140, 140, 255));
    p.setColor(QPalette::Normal,   QPalette::ToolTipBase, QColor(60, 60, 60, 255));
    p.setColor(QPalette::Normal,   QPalette::ToolTipText, QColor(180, 180, 180, 255));
    p.setColor(QPalette::Disabled, QPalette::Foreground, QColor(68, 68, 68, 255));
    p.setColor(QPalette::Disabled, QPalette::Button, QColor(116, 116, 116, 255));
    p.setColor(QPalette::Disabled, QPalette::Light, QColor(159, 159, 159, 255));
    p.setColor(QPalette::Disabled, QPalette::Midlight, QColor(142, 142, 142, 255));
    p.setColor(QPalette::Disabled, QPalette::Dark, QColor(62, 62, 62, 255));
    p.setColor(QPalette::Disabled, QPalette::Mid, QColor(108, 108, 108, 255));
    p.setColor(QPalette::Disabled, QPalette::Text, QColor(94, 94, 94, 255));
    p.setColor(QPalette::Disabled, QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Disabled, QPalette::ButtonText, QColor(57, 57, 57, 255));
    p.setColor(QPalette::Disabled, QPalette::Base, QColor(160, 160, 160, 255));
    p.setColor(QPalette::Disabled, QPalette::Window, QColor(128, 128, 128, 255));
    p.setColor(QPalette::Disabled, QPalette::Shadow, QColor(42, 42, 42, 255));
    p.setColor(QPalette::Disabled, QPalette::Highlight, QColor(128, 128, 128, 255));
    p.setColor(QPalette::Disabled, QPalette::HighlightedText, QColor(68, 68, 68, 255));
    p.setColor(QPalette::Disabled, QPalette::Link, QColor(86, 106, 78, 255));
    p.setColor(QPalette::Disabled, QPalette::LinkVisited, QColor(75, 73, 110, 255));
    p.setColor(QPalette::Disabled, QPalette::AlternateBase, QColor(140, 140, 140, 255));
    p.setColor(QPalette::Disabled, QPalette::ToolTipBase, QColor(60, 60, 60, 255));
    p.setColor(QPalette::Disabled, QPalette::ToolTipText, QColor(180, 180, 180, 255));
    p.setColor(QPalette::Inactive, QPalette::Foreground, QColor(20, 20, 20, 255));
    p.setColor(QPalette::Inactive, QPalette::Button, QColor(116, 116, 116, 255));
    p.setColor(QPalette::Inactive, QPalette::Light, QColor(159, 159, 159, 255));
    p.setColor(QPalette::Inactive, QPalette::Midlight, QColor(142, 142, 142, 255));
    p.setColor(QPalette::Inactive, QPalette::Dark, QColor(62, 62, 62, 255));
    p.setColor(QPalette::Inactive, QPalette::Mid, QColor(108, 108, 108, 255));
    p.setColor(QPalette::Inactive, QPalette::Text, QColor(40, 40, 40, 255));
    p.setColor(QPalette::Inactive, QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Inactive, QPalette::ButtonText, QColor(10, 10, 10, 255));
    p.setColor(QPalette::Inactive, QPalette::Base, QColor(160, 160, 160, 255));
    p.setColor(QPalette::Inactive, QPalette::Window, QColor(128, 128, 128, 255));
    p.setColor(QPalette::Inactive, QPalette::Shadow, QColor(42, 42, 42, 255));
    p.setColor(QPalette::Inactive, QPalette::Highlight, QColor(104, 119, 137, 255));
    p.setColor(QPalette::Inactive, QPalette::HighlightedText, QColor(20, 20, 20, 255));
    p.setColor(QPalette::Inactive, QPalette::Link, QColor(18, 64, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::LinkVisited, QColor(5, 0, 82, 255));
    p.setColor(QPalette::Inactive, QPalette::AlternateBase, QColor(140, 140, 140, 255));
    p.setColor(QPalette::Inactive, QPalette::ToolTipBase, QColor(60, 60, 60, 255));
    p.setColor(QPalette::Inactive, QPalette::ToolTipText, QColor(180, 180, 180, 255));
    return p;
}

QPalette Themes::initIced()
{
    QPalette p;
    p.setColor(QPalette::Normal,   QPalette::Foreground, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Normal,   QPalette::Button, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::Light, QColor(211, 211, 211, 255));
    p.setColor(QPalette::Normal,   QPalette::Midlight, QColor(233, 233, 233, 255));
    p.setColor(QPalette::Normal,   QPalette::Dark, QColor(185, 185, 185, 255));
    p.setColor(QPalette::Normal,   QPalette::Mid, QColor(211, 211, 211, 255));
    p.setColor(QPalette::Normal,   QPalette::Text, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Normal,   QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::ButtonText, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Normal,   QPalette::Base, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::Window, QColor(252, 252, 252, 255));
    p.setColor(QPalette::Normal,   QPalette::Shadow, QColor(134, 134, 134, 255));
    p.setColor(QPalette::Normal,   QPalette::Highlight, QColor(176, 192, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::HighlightedText, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Normal,   QPalette::Link, QColor(0, 0, 192, 255));
    p.setColor(QPalette::Normal,   QPalette::LinkVisited, QColor(88, 0, 176, 255));
    p.setColor(QPalette::Normal,   QPalette::AlternateBase, QColor(252, 252, 252, 255));
    p.setColor(QPalette::Normal,   QPalette::ToolTipBase, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Normal,   QPalette::ToolTipText, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Disabled, QPalette::Foreground, QColor(164, 164, 164, 255));
    p.setColor(QPalette::Disabled, QPalette::Button, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Disabled, QPalette::Light, QColor(211, 211, 211, 255));
    p.setColor(QPalette::Disabled, QPalette::Midlight, QColor(233, 233, 233, 255));
    p.setColor(QPalette::Disabled, QPalette::Dark, QColor(185, 185, 185, 255));
    p.setColor(QPalette::Disabled, QPalette::Mid, QColor(211, 211, 211, 255));
    p.setColor(QPalette::Disabled, QPalette::Text, QColor(166, 166, 166, 255));
    p.setColor(QPalette::Disabled, QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Disabled, QPalette::ButtonText, QColor(166, 166, 166, 255));
    p.setColor(QPalette::Disabled, QPalette::Base, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Disabled, QPalette::Window, QColor(252, 252, 252, 255));
    p.setColor(QPalette::Disabled, QPalette::Shadow, QColor(134, 134, 134, 255));
    p.setColor(QPalette::Disabled, QPalette::Highlight, QColor(252, 252, 252, 255));
    p.setColor(QPalette::Disabled, QPalette::HighlightedText, QColor(164, 164, 164, 255));
    p.setColor(QPalette::Disabled, QPalette::Link, QColor(166, 166, 233, 255));
    p.setColor(QPalette::Disabled, QPalette::LinkVisited, QColor(197, 166, 228, 255));
    p.setColor(QPalette::Disabled, QPalette::AlternateBase, QColor(252, 252, 252, 255));
    p.setColor(QPalette::Disabled, QPalette::ToolTipBase, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Disabled, QPalette::ToolTipText, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::Foreground, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::Button, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Inactive, QPalette::Light, QColor(211, 211, 211, 255));
    p.setColor(QPalette::Inactive, QPalette::Midlight, QColor(233, 233, 233, 255));
    p.setColor(QPalette::Inactive, QPalette::Dark, QColor(185, 185, 185, 255));
    p.setColor(QPalette::Inactive, QPalette::Mid, QColor(211, 211, 211, 255));
    p.setColor(QPalette::Inactive, QPalette::Text, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::BrightText, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Inactive, QPalette::ButtonText, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::Base, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Inactive, QPalette::Window, QColor(252, 252, 252, 255));
    p.setColor(QPalette::Inactive, QPalette::Shadow, QColor(134, 134, 134, 255));
    p.setColor(QPalette::Inactive, QPalette::Highlight, QColor(228, 233, 255, 255));
    p.setColor(QPalette::Inactive, QPalette::HighlightedText, QColor(0, 0, 0, 255));
    p.setColor(QPalette::Inactive, QPalette::Link, QColor(0, 0, 192, 255));
    p.setColor(QPalette::Inactive, QPalette::LinkVisited, QColor(88, 0, 176, 255));
    p.setColor(QPalette::Inactive, QPalette::AlternateBase, QColor(252, 252, 252, 255));
    p.setColor(QPalette::Inactive, QPalette::ToolTipBase, QColor(255, 255, 255, 255));
    p.setColor(QPalette::Inactive, QPalette::ToolTipText, QColor(0, 0, 0, 255));
    return p;
}
