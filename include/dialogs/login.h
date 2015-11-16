#ifndef LOGIN_H
#define LOGIN_H

#include "include/nframecontainer.h"

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
#include <QSettings>
#include <QVariant>
#include <QHash>

class LogIn : public QDialog
{
    Q_OBJECT

public:
    explicit LogIn(QWidget* parent = 0);
    QString getUserName();
    QString getPassword();
    QString getServerName();
    qint16  getServerPort();
    void saveLoginState();

private:
    QLineEdit*	 user_name;
    QLineEdit*	 user_pass;
    QLineEdit*	 server_name;
    QSpinBox*    server_port;
    QPushButton* ok_but;
    void restoreForm();

    QString default_name;
    QString default_server;
    int default_port;

private slots:
    void isValid();

signals:
    void tryValidate();
};

#endif // LOGIN_H