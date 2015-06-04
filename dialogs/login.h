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
#include <QRect>
#include <QApplication>
#include <QDesktopWidget>

class LogIn : public QDialog
{
    Q_OBJECT

public:
    explicit LogIn(QWidget* parent);
    QString getUserName();
    QString getPassword();
    QString getServerName();
    qint16  getServerPort();

private:
    QLineEdit*	 user_name;
    QLineEdit*	 user_pass;
    QLineEdit*	 server_name;
    QSpinBox*    server_port;
    QPushButton* ok_but;
    void restoreForm();

private slots:
    void isValid();

signals:
    void tryValidate();
};

#endif // LOGIN_H
