/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

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
#include "temporarydir.h"
#include <stdlib.h>

#include <QDir>

/**
 * Portable (Qt X.X) temporary directory.
 */
TemporaryDir::TemporaryDir(QObject *parent) : QObject(parent) {

    QString tempDir = QDir::tempPath();
    QString tempPath = QDir(tempDir).filePath("sysmo-tmpdir-");
    QDir dir;
    while (true) {
        QString finalTempPath = tempPath + TemporaryDir::getRandomString();
        if (dir.mkdir(finalTempPath)) {
            this->directoryName = finalTempPath;
            break;
        }
    }

}

QString TemporaryDir::path() {

    return this->directoryName;

}

TemporaryDir::~TemporaryDir() {

    TemporaryDir::removeDir(this->directoryName);

}

bool TemporaryDir::removeDir(QString dirName) {

    bool result = true;
    QDir dir(dirName);

    if (dir.exists(dirName)) {

        Q_FOREACH(QFileInfo info, dir.entryInfoList(
                QDir::NoDotAndDotDot |
                QDir::System |
                QDir::Hidden |
                QDir::AllDirs |
                QDir::Files,
                QDir::DirsFirst)) {
            if (info.isDir()) {
                result = removeDir(info.absoluteFilePath());
            } else {
                result = QFile::remove(info.absoluteFilePath());
            }

            if (!result) {
                return result;
            }
        }
        result = dir.rmdir(dirName);
    }
    return result;

}

QString TemporaryDir::getRandomString() {

    const QString possibleCharacters("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");
    const int randomStringLength = 12;

    QString randomString;
    for (int i = 0; i < randomStringLength; ++i) {
        int index = qrand() % possibleCharacters.length();
        QChar nextChar = possibleCharacters.at(index);
        randomString.append(nextChar);
    }
    return randomString;

}
