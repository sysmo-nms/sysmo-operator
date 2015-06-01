#include "login.h"


LogIn::LogIn(QWidget *parent) : QDialog(parent)
{
    this->setModal(true);
    this->setFixedWidth(470);

    this->user_name   = new QLineEdit(this);
    this->user_pass   = new QLineEdit(this);
    this->server_name = new QLineEdit(this);
    this->server_port = new QSpinBox(this);

    QFrame *srv_frame = new QFrame(this);
    QGridLayout *srv_lay = new QGridLayout();
    srv_frame->setLayout(srv_lay);
    srv_lay->setContentsMargins(0,0,0,0);
    srv_lay->addWidget(this->server_name, 0,0);
    srv_lay->addWidget(new QLabel(QString("Port"),this), 0,1);
    srv_lay->addWidget(this->server_port, 0,2);
    srv_lay->setColumnStretch(0,1);
    srv_lay->setColumnStretch(1,0);
    srv_lay->setColumnStretch(2,0);

    QFrame *separator = new QFrame(this);
    separator->setFixedHeight(15);

    QFrame *form_frame = new QFrame(this);
    QFormLayout *form_lay = new QFormLayout();
    form_frame->setLayout(form_lay);
    form_lay->setContentsMargins(0,0,0,0);
    form_lay->addRow(QString("&User Name:"), this->user_name);
    form_lay->addRow(QString("&Password:"), this->user_pass);
    form_lay->addRow(separator);
    form_lay->addRow(QString("&Server"), srv_frame);

    // buttons
    QPushButton *ok_but = new QPushButton(QString("&Log In"), this);
    ok_but->setDefault(true);
    QPushButton *close_but = new QPushButton(QString("&Close"), this);

    QDialogButtonBox *but_box = new QDialogButtonBox(this);
    but_box->addButton(ok_but, QDialogButtonBox::ApplyRole);
    but_box->addButton(close_but, QDialogButtonBox::RejectRole);

    QLabel *banner = new QLabel(this);
    banner->setPixmap(QPixmap(":/ressources/images/custom/login-banner.png"));

    QGridLayout     *main_grid  = new QGridLayout();
    main_grid->setHorizontalSpacing(14);
    main_grid->setVerticalSpacing(22);

    main_grid->addWidget(banner, 0,0,2,1);
    main_grid->addWidget(form_frame, 0,1);
    main_grid->addWidget(but_box, 1,1);
    main_grid->setRowStretch(0,1);
    main_grid->setRowStretch(1,1);
    main_grid->setRowStretch(2,0);
    this->setLayout(main_grid);
}

