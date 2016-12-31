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
#ifndef QJSON_H
#define QJSON_H
#include <QString>
#include <QVariant>
#include <QDebug>

class QJson
{
    Q_FLAGS(EncodeOption EncodeOptions)
    Q_FLAGS(DecodeOption DecodeOptions)

public:
    enum EncodeOption
    {
        EncodeUnknownTypesAsNull = 0x01,
        Compact = 0x02
    };
    Q_DECLARE_FLAGS(EncodeOptions, EncodeOption)

    enum DecodeOption
    {
        DecodeObjectsAsHash = 0x01,
        AllowUnquotedStrings = 0x02,
        AllowMissingComma = 0x04,
        AllowLazyJSON = AllowUnquotedStrings | AllowMissingComma
    };
    Q_DECLARE_FLAGS(DecodeOptions, DecodeOption)


    static QString encode(const QVariant &data, QString *errorMessage = 0, int indentation = 4);
    static QString encode(const QVariant &data, EncodeOptions options, QString *errorMessage = 0, int indentation = 4);

    static QVariant decode(const QString &json, QString *errorMessage = 0);
    static QVariant decode(const QString &json, DecodeOptions options, QString *errorMessage = 0);

private:
    QJson();

    static QString encodeData(const QVariant &data, EncodeOptions options, QString *errorMessage, int indentation, QString currentLinePrefix);
    static QString encodeString(QString data);
    static QString encodeByteArray(QByteArray data);

    static QVariant parseValue(const QString &json, int &index, DecodeOptions options, bool &success, QString *errorMessage);
    template<typename ContainerType>
    static QVariant parseObject(const QString &json, int &index, DecodeOptions options, bool &success, QString *errorMessage);
    static QVariant parseArray(const QString &json, int &index, DecodeOptions options, bool &success, QString *errorMessage);
    static QVariant parseString(const QString &json, int &index, bool &success, QString *errorMessage);
    static QVariant parseUnquotedString(const QString &json, int &index, bool &success, QString *errorMessage);
    static QVariant parseNumber(const QString &json, int &index, bool &success, QString *errorMessage);
    static QVariant parseBool(const QString &json, int &index, bool &success, QString *errorMessage);
    static QVariant parseNull(const QString &json, int &index, bool &success, QString *errorMessage);
    static int skipWhitespace(const QString &json, int &index);
    static bool checkAvailable(const QString &json, int &index, bool &success, QString *errorMessage, int minAvailable = 1);
    static bool checkToken(const QString &json, int &index, bool &success, QString *errorMessage, QString token);
};

#endif // QJSON_H
