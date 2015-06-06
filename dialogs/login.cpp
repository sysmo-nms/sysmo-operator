#include "login.h"

LogIn::LogIn(QWidget* parent) : QDialog(parent)
{
    this->setModal(true);
    this->setFixedWidth(470);
    this->setWindowTitle("Log in");

    this->user_name   = new QLineEdit(this);
    this->user_pass   = new QLineEdit(this);
    this->user_pass->setEchoMode(QLineEdit::Password);
    this->server_name = new QLineEdit(this);
    this->server_port = new QSpinBox(this);
    this->server_port->setRange(1, 65535);

    QFrame*      srv_frame = new QFrame(this);
    QGridLayout* srv_lay   = new QGridLayout();
    srv_frame->setLayout(srv_lay);
    srv_lay->setContentsMargins(0,0,0,0);
    srv_lay->addWidget(this->server_name, 0,0);
    srv_lay->addWidget(new QLabel("Port",this), 0,1);
    srv_lay->addWidget(this->server_port, 0,2);
    srv_lay->setColumnStretch(0,1);
    srv_lay->setColumnStretch(1,0);
    srv_lay->setColumnStretch(2,0);

    QFrame* separator = new QFrame(this);
    separator->setFixedHeight(15);

    QFrame*      form_frame = new QFrame(this);
    QFormLayout* form_lay   = new QFormLayout();
    form_frame->setLayout(form_lay);
    form_lay->setContentsMargins(0,0,0,0);
    form_lay->addRow("&User Name:", this->user_name);
    form_lay->addRow("&Password:", this->user_pass);
    form_lay->addRow(separator);
    form_lay->addRow("&Server", srv_frame);

    // buttons
    ok_but = new QPushButton("&Log In", this);
    QPushButton* cancel_but = new QPushButton("&Cancel", this);
    QObject::connect(
                ok_but, SIGNAL(clicked(bool)),
                this,	SIGNAL(tryValidate()));
    QObject::connect(
                cancel_but, SIGNAL(clicked(bool)),
                this, 		SLOT(reject()));

    QDialogButtonBox* but_box = new QDialogButtonBox(this);
    but_box->addButton(ok_but, 	   QDialogButtonBox::ApplyRole);
    but_box->addButton(cancel_but, QDialogButtonBox::RejectRole);
    ok_but->setDefault(true);

    // connect to isValid
    QLabel* banner = new QLabel(this);
    banner->setPixmap(QPixmap(":/ressources/images/custom/login-banner.png"));
    QObject::connect(
                this->user_name, SIGNAL(textChanged(QString)),
                this,			 SLOT(isValid()));
    QObject::connect(
                this->user_pass, SIGNAL(textChanged(QString)),
                this,			 SLOT(isValid()));
    QObject::connect(
                this->server_name, SIGNAL(textChanged(QString)),
                this,			   SLOT(isValid()));
    // initialize isValid
    this->restoreForm();
    this->isValid();


    QGridLayout* main_grid  = new QGridLayout();
    main_grid->setHorizontalSpacing(14);
    main_grid->setVerticalSpacing(22);

    main_grid->addWidget(banner, 0,0,2,1);
    main_grid->addWidget(form_frame, 0,1);
    main_grid->addWidget(but_box, 1,1);
    main_grid->setRowStretch(0,1);
    main_grid->setRowStretch(1,1);
    main_grid->setRowStretch(2,0);
    this->setLayout(main_grid);
    QRect screen = QApplication::desktop()->screenGeometry();
    this->move(screen.center() - rect().center());
}

QString LogIn::getUserName()
{
    return this->user_name->text();
}


QString LogIn::getPassword()
{
    return this->user_pass->text();
}


QString LogIn::getServerName()
{
    return this->server_name->text();
}


qint16 LogIn::getServerPort()
{
    return this->server_port->value();
}

void LogIn::restoreForm()
{
    // TODO read setting
    this->user_name->setText("admin");
    this->user_pass->setText("password");
    this->server_name->setText("192.168.0.11");
    this->server_port->setValue(8888);
}

/*
 * SLOTS
 */
void LogIn::isValid()
{
    if (this->user_name->text().isEmpty())
        {this->ok_but->setEnabled(false); return;}
    if (this->user_pass->text().isEmpty())
        {this->ok_but->setEnabled(false); return;}
    if (this->server_name->text().isEmpty())
        {this->ok_but->setEnabled(false); return;}
    this->ok_but->setEnabled(true);
}
