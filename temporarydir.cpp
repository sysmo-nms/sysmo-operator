#include "temporarydir.h"

TemporaryDir::TemporaryDir(QObject *parent) : QObject(parent)
{
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

QString TemporaryDir::path()
{
    return this->directoryName;
}

TemporaryDir::~TemporaryDir()
{
    TemporaryDir::removeDir(this->directoryName);
}

bool TemporaryDir::removeDir(QString dirName)
{
    bool result = true;
    QDir dir(dirName);

    if (dir.exists(dirName)) {
        Q_FOREACH(QFileInfo info, dir.entryInfoList(
                      QDir::NoDotAndDotDot |
                      QDir::System |
                      QDir::Hidden  |
                      QDir::AllDirs |
                      QDir::Files,
                      QDir::DirsFirst)) {
            if (info.isDir()) {
                result = removeDir(info.absoluteFilePath());
            }
            else {
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

QString TemporaryDir::getRandomString()
{
    const QString possibleCharacters("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789");
    const int randomStringLength = 12;

    QString randomString;
    for(int i=0; i<randomStringLength; ++i)
    {
        int index = qrand() % possibleCharacters.length();
        QChar nextChar = possibleCharacters.at(index);
        randomString.append(nextChar);
    }
    return randomString;
}
