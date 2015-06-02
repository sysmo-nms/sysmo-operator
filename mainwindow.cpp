#include "mainwindow.h"


MainWindow::MainWindow(QWidget *parent)
        : QMainWindow(parent)
{
    this->setWindowIcon(QIcon(":/ressources/images/32/logo.png"));
    this->setWindowTitle(QString("Sysmo Operator"));
    this->setObjectName("MainWindow");
    this->setCentralWidget(new CentralWidget(this));
    this->statusBar()->show();

    // TODO init QMessageLogger

    QMenuBar *menu_bar  = this->menuBar();
    QMenu    *main_menu = menu_bar->addMenu(QString("Sysmo"));
    QAction  *action_exit = new QAction(QString("&Exit"), this);
    action_exit->setIcon(QIcon(":/ressources/images/32/system-log-out.png"));
    action_exit->setShortcut(QKeySequence(QString("Ctrl+Q")));
    QObject::connect(
                action_exit, SIGNAL(triggered(bool)),
                this,        SLOT(close()));
    QAction  *action_proxy_conf  = new QAction(QString("&Proxy configuration..."), this);
    QAction  *action_doc_engine  = new QAction(QString("&Configure doc engine..."),this);
    QAction  *action_updates     = new QAction(QString("&Check for updates..."), this);
    QAction  *action_full_screen = new QAction(QString("&Full screen"), this);
    action_full_screen->setIcon(QIcon(":/ressources/images/32/view-fullscreen.png"));
    action_full_screen->setShortcut(QKeySequence(QString("Ctrl+F")));
    QObject::connect(
                action_full_screen, SIGNAL(triggered(bool)),
                this,               SLOT(toggleFullScreen()));
    main_menu->addAction(action_full_screen);
    QMenu *color_menu = main_menu->addMenu(QString("Color theme"));
    main_menu->addSeparator();
    main_menu->addAction(action_proxy_conf);
    main_menu->addAction(action_doc_engine);
    main_menu->addAction(action_updates);
    main_menu->addSeparator();
    main_menu->addAction(action_exit);


    QAction *theme_nat = new QAction(QString("Native"), this);
    QAction *theme_mid = new QAction(QString("Midnight"), this);
    QAction *theme_inl = new QAction(QString("Inland"), this);
    QAction *theme_gre = new QAction(QString("Greys"), this);
    QAction *theme_sno = new QAction(QString("Snowy"), this);
    theme_nat->setCheckable(true);
    theme_mid->setCheckable(true);
    theme_inl->setCheckable(true);
    theme_gre->setCheckable(true);
    theme_sno->setCheckable(true);
    QActionGroup *color_group = new QActionGroup(this);
    color_group->addAction(theme_nat);
    color_group->addAction(theme_mid);
    color_group->addAction(theme_inl);
    color_group->addAction(theme_gre);
    color_group->addAction(theme_sno);
    color_group->setExclusive(true);
    color_menu->addAction(theme_nat);
    color_menu->addSeparator();
    color_menu->addAction(theme_mid);
    color_menu->addAction(theme_inl);
    color_menu->addAction(theme_gre);
    color_menu->addAction(theme_sno);
    color_menu->setIcon(QIcon(":/ressources/images/32/preferences-desktop-theme.png"));
    theme_nat->setChecked(true);
    this->hide();

    this->log_in_dialog = new LogIn(this);
    QObject::connect(
                this->log_in_dialog, SIGNAL(rejected()),
                this,				 SLOT(close()));
    QObject::connect(
                this->log_in_dialog, SIGNAL(tryValidate()),
                this,				 SLOT(tryValidate()));
    this->log_in_dialog->open();
}


MainWindow::~MainWindow()
{

}


/*
 * SLOTS
 */
void MainWindow::toggleFullScreen()
{
    if (this->isFullScreen()) {
        this->showNormal();
    } else {
        this->showFullScreen();
    }
}


/*
 * Triggered by LogIn validate button.
 */
void MainWindow::tryValidate()
{
    std::cout << "try validate" << std::endl;
    this->log_in_dialog->setEnabled(false);
    this->supercast = new Supercast(this);
    QObject::connect(
                this->supercast, SIGNAL(connexionStatus(int)),
                this, 			 SLOT(connexionStatus(int)));
    this->supercast->tryConnect(
        QHostAddress(QString("192.168.0.11")),
        (qint16)8888,
        QString("admin"),
        QString("password"));
    //this->log_in_dialog->setEnabled(false);

}

/*
 * Triggered by Supercast. Finalize the connection, or
 * close the application.
 */
void MainWindow::connexionStatus(int status)
{
    std::cout << "Connexion status" << status << std::endl;
    if (status == Supercast::ConnexionSuccess) {
        this->log_in_dialog->close();
        this->show();
        return;
    }

    QMessageBox err_box;
    err_box.setModal(true);
    err_box.setIcon(QMessageBox::Critical);
    this->setEnabled(false);
    switch(status) {
        case Supercast::AuthenticationError: {
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
            err_box.setText("The remote host closed the connexion.");
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
