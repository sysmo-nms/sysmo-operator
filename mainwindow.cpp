#include "mainwindow.h"

QSize MainWindow::sizeHint() const {return this->default_size;}

MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent)
{
    /*
     * Initialize supercast.
     */
    this->supercast = new Supercast(this);


    /*
     * Initialize rrd4c-> Will effectively start the java rrd4qt process.
     */
    this->rrd4c     = new Rrd4Qt(this);


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
    QMenu*    main_menu = menu_bar->addMenu("Sysmo");

    QAction* action_exit = new QAction("&Exit", this);
    action_exit->setIcon(QIcon(":/icons/system-log-out.png"));
    action_exit->setShortcut(QKeySequence("Ctrl+Q"));
    QObject::connect(
                action_exit, SIGNAL(triggered(bool)),
                this,        SLOT(close()));

    QAction* action_proxy_conf  = new QAction("&Proxy configuration...",  this);
    QAction* action_doc_engine  = new QAction("&Configure doc engine...", this);
    QAction* action_updates     = new QAction("&Check for updates...",    this);
    QAction* action_full_screen = new QAction("&Full screen",             this);
    action_full_screen->setIcon(QIcon(":/icons/view-fullscreen.png"));
    action_full_screen->setShortcut(QKeySequence("Ctrl+F"));
    QObject::connect(
                action_full_screen, SIGNAL(triggered(bool)),
                this,               SLOT(toggleFullScreen()));

    main_menu->addAction(action_full_screen);
    QMenu* color_menu = main_menu->addMenu("Color theme");
    main_menu->addSeparator();
    main_menu->addAction(action_proxy_conf);
    main_menu->addAction(action_doc_engine);
    main_menu->addAction(action_updates);
    main_menu->addSeparator();
    main_menu->addAction(action_exit);

    QAction* theme_nat = new QAction("Native",   this);
    QAction* theme_mid = new QAction("Midnight", this);
    QAction* theme_inl = new QAction("Inland",   this);
    QAction* theme_gre = new QAction("Greys",    this);
    QAction* theme_ice = new QAction("Iced",     this);
    theme_nat->setCheckable(true);
    theme_mid->setCheckable(true);
    theme_inl->setCheckable(true);
    theme_gre->setCheckable(true);
    theme_ice->setCheckable(true);
    QActionGroup* color_group = new QActionGroup(this);
    color_group->addAction(theme_nat);
    color_group->addAction(theme_mid);
    color_group->addAction(theme_inl);
    color_group->addAction(theme_gre);
    color_group->addAction(theme_ice);
    color_group->setExclusive(true);
    color_menu->addAction(theme_nat);
    color_menu->addSeparator();
    color_menu->addAction(theme_mid);
    color_menu->addAction(theme_inl);
    color_menu->addAction(theme_gre);
    color_menu->addAction(theme_ice);
    color_menu->setIcon(QIcon(":/icons/preferences-desktop-theme.png"));
    theme_nat->setChecked(true);
    /*
     * Fill the menu bar END
     */


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
    this->log_in_dialog = new LogIn(this);
    QObject::connect(
                this->log_in_dialog, SIGNAL(rejected()),
                this,                SLOT(close()));
    QObject::connect(
                this->log_in_dialog, SIGNAL(tryValidate()),
                this,                SLOT(tryValidate()));
    this->log_in_dialog->open();
}



MainWindow::~MainWindow()
{
    /*
     * Save state
     */
}


/*
 * SLOTS
 */
void MainWindow::toggleFullScreen()
{
    if (this->isFullScreen()) this->showNormal();
    else                      this->showFullScreen();
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
    if (status == Supercast::CONNECTION_SUCCESS) {
        this->log_in_dialog->close();
        this->show();
        return;
    }

    MessageBox err_box;
    err_box.setModal(true);
    err_box.setIconType(Sysmo::MESSAGE_ERROR);
    err_box.setStandardButtons(QMessageBox::Close);
    this->setEnabled(false);
    switch(status) {
        case Supercast::AUTHENTICATION_ERROR: {
            err_box.setText("Authentication failure.");
            err_box.setInformativeText("The authentication procedure has failed. Check your password or username.");
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
    this->close();
}
