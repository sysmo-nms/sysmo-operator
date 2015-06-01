#ifndef LOGIN_H
#define LOGIN_H

#include "nframecontainer.h"

#include <QObject>
#include <QWidget>
#include <QDialog>
#include <QLineEdit>
#include <QSpinBox>
#include <QFrame>
#include <QGridLayout>
#include <QFormLayout>
#include <QPushButton>
#include <QLabel>
#include <QDialogButtonBox>
#include <QPixmap>

class LogIn : public QDialog
{
    Q_OBJECT

public:
    explicit LogIn(QWidget *parent);
private:
    QLineEdit *user_name;
    QLineEdit *user_pass;
    QLineEdit *server_name;
    QSpinBox  *server_port;
};

#endif // LOGIN_H
