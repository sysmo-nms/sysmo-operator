#include "mainwindow.h"

QSize MainWindow::sizeHint() const {return this->default_size;}

MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent)
{
    this->log_in_dialog = new LogIn(this);
}

QWidget* MainWindow::getLoginWindow()
{
    return this->log_in_dialog;
}

void MainWindow::initSysmo() {
    /*
     * Initialize supercast.
     */
    this->supercast = new Supercast(this);


    /*
     * Initialize rrd4c-> Will effectively start the java rrd4qt process.
     */
    this->rrd4c = new Rrd4Qt(this);

    /*
     * Init SystemTray
     */
    this->system_tray = new SystemTray(this);

    /*
     * Generic things
     */
    this->setWindowIcon(QIcon(":/icons/logo.png"));
    this->setCentralWidget(new CentralWidget(this));
    this->statusBar()->show();


    /*
     * Fill the menu bar
     */

    QMenuBar* menu_bar  = this->menuBar();
    // Sysmo menu
    QMenu*    main_menu = menu_bar->addMenu("Sysmo");

    QAction* action_exit = new QAction("&Exit", this);
    action_exit->setIcon(QIcon(":/icons/system-log-out.png"));
    action_exit->setShortcut(QKeySequence("Ctrl+Q"));
    QObject::connect(
                action_exit, SIGNAL(triggered(bool)),
                this,        SLOT(close()));

    //QAction* action_proxy_conf  = new QAction("&Proxy configuration...",  this);
    QAction* action_doc_engine  = new QAction("&Configure doc engine...", this);
    QObject::connect(
                action_doc_engine, SIGNAL(triggered(bool)),
                this, SLOT(configureDocEngine()));
    //QAction* action_updates     = new QAction("&Check for updates...",    this);
    QAction* action_full_screen = new QAction("&Full screen",             this);
    action_full_screen->setIcon(QIcon(":/icons/view-fullscreen.png"));
    action_full_screen->setShortcut(QKeySequence("Ctrl+F"));
    QObject::connect(
                action_full_screen, SIGNAL(triggered(bool)),
                this,               SLOT(toggleFullScreen()));

    main_menu->addAction(action_full_screen);
    QMenu* color_menu = main_menu->addMenu("Color theme");
    main_menu->addSeparator();
    //main_menu->addAction(action_proxy_conf);
    //main_menu->addAction(action_doc_engine);
    //main_menu->addAction(action_updates);
    main_menu->addSeparator();
    main_menu->addAction(action_exit);

    QAction* theme_nat = new QAction("Native",   this);
    theme_nat->setData(QVariant("native"));
    theme_nat->setCheckable(true);
    QAction* theme_mid = new QAction("Midnight", this);
    theme_mid->setData(QVariant("midnight"));
    theme_mid->setCheckable(true);
    QAction* theme_inl = new QAction("Inland",   this);
    theme_inl->setData(QVariant("inland"));
    theme_inl->setCheckable(true);
    QAction* theme_gre = new QAction("Greys",    this);
    theme_gre->setData(QVariant("greys"));
    theme_gre->setCheckable(true);
    QAction* theme_ice = new QAction("Iced",     this);
    theme_ice->setData(QVariant("iced"));
    theme_ice->setCheckable(true);
    this->color_group = new QActionGroup(this);
    this->color_group->addAction(theme_nat);
    this->color_group->addAction(theme_mid);
    this->color_group->addAction(theme_inl);
    this->color_group->addAction(theme_gre);
    this->color_group->addAction(theme_ice);
    this->color_group->setExclusive(true);
    QObject::connect(
                this->color_group, SIGNAL(triggered(QAction*)),
                this,        SLOT(setThemeConfig(QAction*)));
    color_menu->addAction(theme_nat);
    color_menu->addSeparator();
    color_menu->addAction(theme_mid);
    color_menu->addAction(theme_inl);
    color_menu->addAction(theme_gre);
    color_menu->addAction(theme_ice);
    color_menu->setIcon(QIcon(":/icons/preferences-desktop-theme.png"));
    theme_nat->setChecked(true);
    // Fill sysmo menu bar END

    QMenu* help_menu = menu_bar->addMenu("Help");

    QAction* help = new QAction("Get help...", this);
    help->setIcon(QIcon(":/icons/help-browser.png"));
    QObject::connect(
                help, SIGNAL(triggered(bool)),
                this, SLOT(handleHelpAction()));

    QAction* sysmo_io = new QAction("Sysmo main website...", this);
    QObject::connect(
                sysmo_io, SIGNAL(triggered(bool)),
                this, SLOT(handleMainWebsiteAction()));

    QAction* about = new QAction("About Sysmo...", this);
    QObject::connect(
                about, SIGNAL(triggered(bool)),
                this, SLOT(handleAboutAction()));

    help_menu->addAction(help);
    help_menu->addAction(sysmo_io);
    help_menu->addSeparator();
    help_menu->addAction(about);

    /*
     * Initialize acceptable default. Will be overriden by saveState and
     * restore state after the first app start.
     */
    this->default_size = QSize(1040,585);


    /*
     * Be sure to not be shown before the log in dialog
     */
    this->hide();


    /*
     * Set up supercast signals and slots.
     */
    MonitorWidget* monitor = MonitorWidget::getInstance();
    QObject::connect(
                this->supercast, SIGNAL(connectionStatus(int)),
                monitor,         SLOT(connectionStatus(int)));

    QObject::connect(
                this->supercast, SIGNAL(connectionStatus(int)),
                this,            SLOT(connectionStatus(int)));


    /*
     * create, connect and open the log_in_dialog
     * Note that on log_in failure, the entire application close.
     */
    QObject::connect(
                this->log_in_dialog, SIGNAL(rejected()),
                this,                SLOT(close()));
    QObject::connect(
                this->log_in_dialog, SIGNAL(tryValidate()),
                this,                SLOT(tryValidate()));
    this->log_in_dialog->open();

    this->restoreStateFromSettings();
}


MainWindow::~MainWindow()
{
    QSettings s;
    s.setValue("main/geometry", this->saveGeometry());
}

void MainWindow::restoreStateFromSettings()
{
    /*
     * Restaure color theme
     */
    QSettings s;
    QVariant v = s.value("color_theme");
    if (v.isValid()) {
        QString theme = v.toString();
        QList<QAction*> action_list = this->color_group->actions();
        foreach (QAction* ac, action_list) {
            if (theme == ac->data().toString()) {
                ac->setChecked(true);
                break;
            }
        }
    }

    QVariant geom = s.value("main/geometry");
    if (geom.isValid()) {
        this->restoreGeometry(geom.toByteArray());
    }
}

/*
 * SLOTS
 */
void MainWindow::configureDocEngine()
{

}

void MainWindow::toggleFullScreen()
{
    if (this->isFullScreen()) this->showNormal();
    else                      this->showFullScreen();
}

void MainWindow::setThemeConfig(QAction *theme)
{
    QSettings s;
    s.setValue("color_theme", theme->data());
    MessageBox msgbox(this);
    msgbox.setIconType(Sysmo::MESSAGE_INFO);
    msgbox.setText("Color theme is succesfully modified. You must restart the application to make it effective.");
    msgbox.setInformativeText("Do you want to restart now?");
    msgbox.setStandardButtons(QMessageBox::Yes | QMessageBox::No);
    msgbox.setDefaultButton(QMessageBox::Yes);
    int ret = msgbox.exec();
    if (ret == QMessageBox::Yes) {
        QCoreApplication::exit(Sysmo::APP_RESTART_CODE);
    }
}


/*
 * Triggered by LogIn validate button.
 */
void MainWindow::tryValidate()
{
    this->log_in_dialog->setEnabled(false);
    QString   user(this->log_in_dialog->getUserName());
    QString   pass(this->log_in_dialog->getPassword());
    QString server(this->log_in_dialog->getServerName());
    qint16    port(this->log_in_dialog->getServerPort());

    this->supercast->tryConnect(QHostAddress(server), port, user, pass);
}


/*
 * Triggered by Supercast. Finalize the connection, or
 * close the application.
 */
void MainWindow::connectionStatus(int status)
{
    qDebug() << "conn status: " << status;
    if (status == Supercast::CONNECTION_SUCCESS) {
        this->log_in_dialog->saveLoginState();
        this->log_in_dialog->close();
        this->show();
        return;
    }

    this->log_in_dialog->close();
    MessageBox err_box;
    err_box.setModal(true);
    err_box.setIconType(Sysmo::MESSAGE_ERROR);
    err_box.setStandardButtons(QMessageBox::Close);
    this->setEnabled(false);
    switch(status) {
        case Supercast::AUTHENTICATION_ERROR: {
            err_box.setText("Authentication failure.");
            err_box.setInformativeText("The authentication procedure has failed.");
            break;
        }
        case QAbstractSocket::ConnectionRefusedError: {
            err_box.setText("The connection was refused by the peer.");
            err_box.setInformativeText("You may trying to connect to the wrong host, or the wrong port.");
            break;
        }
        case QAbstractSocket::RemoteHostClosedError: {
            err_box.setText("The remote host closed the connection.");
            err_box.setInformativeText("This can append if the host came down, or if the service is restarting.");
            break;
        }
        case QAbstractSocket::HostNotFoundError: {
            err_box.setText("Host not found.");
            err_box.setInformativeText("Cannot resolve hostname.");
            break;
        }
        case QAbstractSocket::SocketTimeoutError: {
            err_box.setText("Socket timed out.");
            err_box.setInformativeText("You may trying to connect to the wrong host, or the wrong port.");
            break;
        }
        case QAbstractSocket::NetworkError: {
            err_box.setText("Network error.");
            err_box.setInformativeText("Can not reach the host.");
            break;
        }
        default: {
            err_box.setText("Unknown socket Error");
        }
    }

    err_box.exec();
    QCoreApplication::exit(1);
}

void MainWindow::handleAboutAction()
{
    QString msg;
    msg += "Copyright (c) 2012-2015 Sebastien Serre <ssbx@sysmo.io>\n\n";
    msg += "Sysmo NMS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\n";
    msg += "Sysmo NMS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.\n\n";
    msg += "You should have received a copy of the GNU General Public License along with Sysmo.  If not, see <http://www.gnu.org/licenses/>.";


    QMessageBox::about(this, "Sysmo NMS (www.sysmo.io)", msg);
}

void MainWindow::handleMainWebsiteAction()
{
    QDesktopServices::openUrl(QUrl("http://www.sysmo.io"));
}

void MainWindow::handleHelpAction()
{
    QDesktopServices::openUrl(QUrl("http://www.sysmo.io/Community"));
}
