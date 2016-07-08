/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>

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
#include "login.h"


LogIn::LogIn(QWidget* parent) : QDialog(parent)
{

    this->setWindowFlags(this->windowFlags() | Qt::WindowStaysOnTopHint);

    this->default_name = "admin";
    this->default_port = 9758;
    this->default_server = "127.0.0.1";

    this->setModal(true);
    this->setFixedWidth(470);
    this->setWindowTitle("Log in");

    this->user_name   = new LineEdit(this);
    this->user_pass   = new LineEdit(this);
    this->user_pass->setEchoMode(LineEdit::Password);
    this->server_name = new LineEdit(this);
    this->server_port = new QSpinBox(this);
    this->server_port->setRange(1, 65535);

    QFrame*      srv_frame = new QFrame(this);
    QGridLayout* srv_lay   = new QGridLayout();
    srv_frame->setLayout(srv_lay);
    srv_lay->setContentsMargins(0,0,0,0);
    srv_lay->addWidget(this->server_name, 0,0);
#ifdef USE_WEBSOCKET
    this->default_port = 8080;
    srv_lay->addWidget(new QLabel("HTTP Port",this), 0,1);
#else
    srv_lay->addWidget(new QLabel("TCP Port",this), 0,1);
#endif
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
    but_box->addButton(ok_but, 	   QDialogButtonBox::AcceptRole);
    but_box->addButton(cancel_but, QDialogButtonBox::RejectRole);
    ok_but->setDefault(true);

    // connect to isValid
    QLabel* banner = new QLabel(this);
    banner->setPixmap(QPixmap(":/images/login-banner.png"));
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

    QSettings s;

    QVariant var = s.value("login/login_state");
    QHash<QString, QVariant> login_state;
    if (!var.isValid()) {
        login_state.insert("name", this->default_name);
        login_state.insert("server", this->default_server);
        login_state.insert("port", this->default_port);
        login_state.insert("password", QVariant(""));
        s.setValue("login/login_state", QVariant(login_state));
    } else {
        login_state = var.toHash();
    }
    this->user_name->setText(login_state.value("name").toString());
    this->user_pass->setText(login_state.value("password").toString());
    this->server_name->setText(login_state.value("server").toString());
    this->server_port->setValue(login_state.value("port").toInt());

}


void LogIn::saveLoginState()
{

    qDebug() << "save login state" << this->server_name->text();
    qDebug() << "save login state" << this->server_port->value();
    QSettings s;
    QHash<QString, QVariant> lstate = s.value("login/login_state").toHash();
    lstate.insert("name", QVariant(this->user_name->text()));
    lstate.insert("server", QVariant(this->server_name->text()));
    lstate.insert("password", QVariant(this->user_pass->text()));
    lstate.insert("port", QVariant(this->server_port->value()));
    s.setValue("login/login_state", QVariant(lstate));

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
