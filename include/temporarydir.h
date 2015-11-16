#ifndef TEMPORARYDIR_H
#define TEMPORARYDIR_H

#include <stdlib.h>

#include <QObject>
#include <QString>
#include <QDir>


class TemporaryDir : public QObject
{

public:
    explicit TemporaryDir(QObject *parent = 0);
    ~TemporaryDir();
    QString path();

private:
    QString directoryName;
    static bool removeDir(QString dirName);
    static QString getRandomString();

};

#endif // TEMPORARYDIR_H
