#include "include/lineedit.h"

LineEdit::LineEdit(QWidget* parent) : QLineEdit(parent)
{

}

#if QT_VERSION < 0x040700
void LineEdit::setPlaceholderText(const QString str)
{
    Q_UNUSED(str);
}
#endif
