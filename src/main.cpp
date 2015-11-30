/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

Sysmo NMS is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sysmo NMS is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.
*/
#include "stdio.h"
#include "stdlib.h"

#include "include/mainwindow.h"
#include "include/themes.h"
#include "include/sysmo.h"
#include "include/rotatingfilelogger.h"

#include <QApplication>
#include <QSettings>
#include <QIcon>
#include <QtGlobal>
#include <QSettings>
#include <QVariant>

int main(int argc, char* argv[])
{

        int RETURN_CODE;
        do {
                QString version = "1.1.0";

                QApplication::setApplicationName("Sysmo Operator");
                QApplication::setApplicationVersion(version);
                QApplication::setOrganizationName("Sysmo NMS");
                QApplication::setOrganizationDomain("sysmo.io");
                QApplication::setQuitOnLastWindowClosed(true);
                QSettings settings;
                QVariant variant = settings.value("color_theme");
                if (variant.isValid()) {
                        QString theme = variant.toString();
                        if (theme == "midnight") {
                                QApplication::setPalette(Themes::midnight);
                        } else if (theme == "inland") {
                                QApplication::setPalette(Themes::inland);
                        } else if (theme == "greys") {
                                QApplication::setPalette(Themes::greys);
                        } else if (theme == "iced") {
                                QApplication::setPalette(Themes::iced);
                        }
                }

                QApplication app(argc, argv);
                RotatingFileLogger::getLogger()->setParent(&app);

#if QT_VERSION >= 0x050000
                //qInstallMessageHandler(RotatingFileLogger::log);
                QApplication::setStyle("fusion");
#else
                //qInstallMsgHandler(RotatingFileLogger::log);
                QApplication::setStyle("plastique");
#endif

                app.setWindowIcon(QIcon(":/icons/logo.png"));

                MainWindow w;

                RETURN_CODE = app.exec();
#if QT_VERSION < 0x050000
                if (RETURN_CODE == Sysmo::APP_RESTART_CODE) {
                    // TODO make app restart working with qt4
                    RETURN_CODE = 0;
                }
#endif
        } while (RETURN_CODE == Sysmo::APP_RESTART_CODE);

        return RETURN_CODE;
}
