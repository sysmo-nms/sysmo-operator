#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    this->setWindowIcon(QIcon(":/ressources/images/32/logo.png"));
    this->setWindowTitle(QString("Sysmo Operator"));
    this->setObjectName("MainWindow");
    this->setCentralWidget(new CentralWidget(this));
    this->statusBar()->show();


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
}

void MainWindow::toggleFullScreen()
{
    if (this->isFullScreen()) {
        this->showNormal();
    } else {
        this->showFullScreen();
    }
}

MainWindow::~MainWindow()
{

}
