#ifndef LINEEDIT_H
#define LINEEDIT_H

#include <QLineEdit>

class LineEdit : public QLineEdit
{
public:
    LineEdit(QWidget* parent = 0);
#if QT_VERSION < 0x040700
    void setPlaceholderText(const QString text);
#endif

};

#endif // LINEEDIT_H
