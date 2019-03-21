/*
Sysmo NMS Network Management and Monitoring solution (https://sysmo-nms.github.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

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
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#include <logs/clog.h>
#include "mainwindow.h"
#include "themes.h"
#include "sysmo.h"
#include "config.h"

#include <QApplication>
#include <QSettings>
#include <QIcon>
#include <QtGlobal>
#include <QSettings>
#include <QVariant>
#include <QPointer>
#include <QFile>
#include <QFont>

int
main(int argc, char** argv) {

    if (NULL == clogSetOutput("mylog.log")) {
        fprintf(stderr, "Failed to open log file: %s\n", strerror(errno));
        exit(1);
    }

    int RETURN_CODE;
    do {
        QString version = OPERATOR_VERSION_STR;
        QApplication::setApplicationName("Sysmo Operator");
        QApplication::setApplicationVersion(version);
        QApplication::setOrganizationName("Sysmo NMS");
        QApplication::setOrganizationDomain("sysmo.io");
        QApplication::setQuitOnLastWindowClosed(true);
        QSettings settings;
        bool use_darcula_qss = false;
        QVariant variant = settings.value("color_theme");
        if (variant.isValid()) {
            QString theme = variant.toString();
            Themes::setStyle(theme);
            if (theme == "midnight") {
                //QApplication::setFont(default_font);
                QApplication::setPalette(Themes::midnight);
            } else if (theme == "inland") {
                //QApplication::setFont(default_font);
                QApplication::setPalette(Themes::inland);
            } else if (theme == "greys") {
                //QApplication::setFont(default_font);
                QApplication::setPalette(Themes::greys);
            } else if (theme == "iced") {
                //QApplication::setFont(default_font);
                QApplication::setPalette(Themes::iced);
            } else if (theme == "darcula") {
                use_darcula_qss = true;
            }
        }

        QApplication app(argc, argv);

#if QT_VERSION < 0x050000
        //qInstallMsgHandler(logger...)
        QApplication::setStyle("plastique");
#else
        //qInstallMessageHandler(logger...)
        QApplication::setStyle("fusion");
#endif


        app.setWindowIcon(QIcon(":/icons/logo.png"));

#ifdef USE_WEBSOCKET
        qDebug() << "will use websocket";
#endif
        MainWindow win;
        win.setStyleSheet(Themes::getStyleSheet());

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
