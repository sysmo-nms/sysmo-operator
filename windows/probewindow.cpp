#include "probewindow.h"

QHash<QString,ProbeWindow*> ProbeWindow::windows = QHash<QString,ProbeWindow*>();

ProbeWindow::ProbeWindow(QString probeName)
                        : MonitorProxyWidget(probeName)
{
    this->name = probeName;

    /*
     * Init various element of QWidget. The newly created window is non
     * modal and will cleanly close on application shutdown.
     */
    this->setWindowFlags(this->windowFlags() | Qt::Window);
    this->setWindowModality(Qt::NonModal);
    this->setAttribute(Qt::WA_QuitOnClose, false);


    /*
     * Get the check identifier
     */
    Monitor*      mon = Monitor::getInstance();
    QJsonObject probe = mon->probes->value(this->name);
    QString  probe_id = probe.value("probeId").toString();
    qDebug() << "probe is: " << probe_id;

    /*
     * Read the NChecks XML graph definition.
     */
    QXmlSimpleReader        reader;
    QXmlInputSource*         input = new QXmlInputSource();
    ParseCheckMakeGraphCMD* parser = new ParseCheckMakeGraphCMD();
    input->setData(NChecks::getCheck(probe_id));
    reader.setContentHandler(parser);
    reader.setErrorHandler(parser);
    reader.parse(input);
    QJsonObject config = parser->config;
    qDebug() << "parser return: " << config.keys();
    QJsonObject graphs = config.take("graphs").toObject();
    qDebug() << "parser return: " << config;
    qDebug() << "parser return: " << graphs;
    delete parser;
    delete input;


    /*
     * begin layout
     */
    // top log area controls
    NFrame* log_controls = new NFrame(this);
    NGridContainer*  lc_grid      = new NGridContainer();
    log_controls->setLayout(lc_grid);
    QLabel*    time_line_label = new QLabel("TimeLine:", this);
    QComboBox* time_line_cbox  = new QComboBox(this);
    QLabel*    height_label = new QLabel("Graph height:", this);
    QComboBox* height_cbox  = new QComboBox(this);
    lc_grid->addWidget(time_line_label, 0,0);
    lc_grid->addWidget(time_line_cbox, 0,1);
    lc_grid->addWidget(height_label, 0,2);
    lc_grid->addWidget(height_cbox, 0,3);
    lc_grid->setColumnStretch(0,0);
    lc_grid->setColumnStretch(1,0);
    lc_grid->setColumnStretch(2,0);
    lc_grid->setColumnStretch(3,0);
    lc_grid->setColumnStretch(4,1);

    // bottom log area graphs
    QScrollArea* log_scroll = new QScrollArea(this);
    log_scroll->setAutoFillBackground(true);
    log_scroll->setBackgroundRole(QPalette::Window);
    log_scroll->setFrameShape(QFrame::Panel);
    log_scroll->setFrameShadow(QFrame::Sunken);

    // log area container
    NFrameContainer* log_area = new NFrameContainer(this);
    log_area->setAutoFillBackground(true);
    log_area->setBackgroundRole(QPalette::Light);
    log_area->setFrameShape(QFrame::StyledPanel);
    log_area->setFrameShadow(QFrame::Raised);
    NGrid* log_area_grid = new NGrid();
    log_area_grid->setRowStretch(0,0);
    log_area_grid->setRowStretch(1,1);
    log_area->setLayout(log_area_grid);

    log_area_grid->addWidget(log_controls, 0,0);
    log_area_grid->addWidget(log_scroll, 1,0);

    // status bar
    this->status_bar = new QStatusBar(this);

    // final grid
    NGrid* grid = new NGrid();
    grid->addWidget(log_area, 0,0);
    grid->addWidget(this->status_bar, 1,0);
    grid->setRowStretch(0,1);
    grid->setRowStretch(1,0);
    this->setLayout(grid);
    /*
     * end layout
     */
}

ProbeWindow::~ProbeWindow()
{
    ProbeWindow::windows.remove(this->name);
    /*
     * TODO save state
     */
}

void ProbeWindow::handleEvent(QJsonObject event) {
    qDebug() << "handle event event event:.........................." << event;
}

void ProbeWindow::closeEvent(QCloseEvent* event)
{
    event->accept();
    this->deleteLater();
}

void ProbeWindow::openWindow(QString name)
{
    /*
    //MULTIPLE SUBSCRIBE BEGIN
    ProbeWindow* win = new ProbeWindow(name);
    win->showNormal();
    //TEST CASE END
    */

    ProbeWindow* win = NULL;

    /*
     * If window exist use it. Else create and insert it in
     * ProbeWindow::windows hash.
     */
    if (ProbeWindow::windows.contains(name)) {

        win = ProbeWindow::windows.value(name);

    } else {

        /*
         * Create and register new window.
         */
        win = new ProbeWindow(name);
        ProbeWindow::windows.insert(name, win);

        /*
         * Connect qApp to have a clean application shutdown.
         */
        QObject::connect(
                    qApp, SIGNAL(aboutToQuit()),
                    win,  SLOT(deleteLater()));
    }

    /*
     * Show normal (raize), set focus and show in first Z order.
     */
    win->showNormal();
    win->setFocus();
    qApp->setActiveWindow(win);
}
