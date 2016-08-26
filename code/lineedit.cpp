#include "lineedit.h"

/**
 * Used to stay compatible with Qt4.7 QLineEdit from wich setPlaceholderText
 * is missing
 */
LineEdit::LineEdit(QWidget* parent) : QLineEdit(parent)
{

}

#if QT_VERSION < 0x040700
void
LineEdit::setPlaceholderText(const QString str)
{
    Q_UNUSED(str);
}
#endif
