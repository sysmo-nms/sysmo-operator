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

    this->rrd_config = parser->config;
    delete parser;
    delete input;


    /*
     * begin generic layout
     */
    // top log area controls
    NFrame*    log_controls = new NFrame(this);
    NGridContainer* lc_grid = new NGridContainer();
    log_controls->setLayout(lc_grid);

    QLabel*    time_line_label = new QLabel("TimeLine:", this);
    QComboBox* time_line_cbox  = new QComboBox(this);
    lc_grid->addWidget(time_line_label, 0,0);
    lc_grid->addWidget(time_line_cbox, 0,1);

    QLabel*    height_label = new QLabel("Graph height:", this);
    QComboBox* height_cbox  = new QComboBox(this);
    lc_grid->addWidget(height_label, 0,2);
    lc_grid->addWidget(height_cbox, 0,3);

    lc_grid->setColumnStretch(0,0);
    lc_grid->setColumnStretch(1,0);
    lc_grid->setColumnStretch(2,0);
    lc_grid->setColumnStretch(3,0);
    lc_grid->setColumnStretch(4,1);

    // bottom log area graphs
    this->scroll_area = new QScrollArea(this);
    this->scroll_area->setAutoFillBackground(true);
    this->scroll_area->setBackgroundRole(QPalette::Window);
    this->scroll_area->setFrameShape(QFrame::Panel);
    this->scroll_area->setFrameShadow(QFrame::Sunken);
    this->scroll_area->setMinimumWidth(400);
    this->scroll_area->setMinimumHeight(200);
    this->scroll_area->setWidgetResizable(true);

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
    log_area_grid->addWidget(this->scroll_area, 1,0);

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
     * end generic layout
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
    /*
     * If event is "update"
     */
    if (event.value("event").toString() == "update")
    {
        return;
    }

    /*
     * If event is "dump". Occur only one time.
     */
    if (event.value("event").toString() != "dump")
    {
        qWarning() << "unknown event:" << event;
        return;
    }

    /*
     * "frame" will be the child of "this->scroll_area"
     */
    NFrame* frame = new NFrame();
    NGrid*   grid = new NGrid();
    frame->setLayout(grid);


    /*
     * If type is "simple".
     */
    if (event.value("type").toString() == "simple")
    {
        QJsonObject js_graphs = this->rrd_config.value("graphs").toObject();

        /*
         * initialize grid row
         */
        int row = 0;

        /*
         * Get graphs key and sort them
         */
        QStringList keys = js_graphs.keys();
        keys.sort();

        /*
         * Then iterate sorted keys
         */
        QStringListIterator i(keys);
        while (i.hasNext())
        {
            QString key = i.next();

            /*
             * From there, the Rrd4QtGraph() will handle himself showing
             * the graph defined.
             */
            Rrd4QtGraph* graph = new Rrd4QtGraph(
                            event.value("rrdFile").toString(), // rrd db
                            js_graphs.value(key).toObject(),   // graph def
                            frame);                            // parent

            graph->setFixedHeight(300);

            grid->addWidget(graph, row, 0);

            ++row;
        }

        /*
         * Set the scroll area newly created widget
         */
        this->scroll_area->setWidget(frame);

        /*
         * From the "QScrollArea.setWidget(QWidget)" doc, added widget must
         * explicitely be show().
         */
        qDebug() << "simple draw " << event;
        frame->show();
        return;
    }




    /*
     * Else it must be a "table"
     */
    if (event.value("type").toString() == "table")
    {
        /*
         * Get rrd file index
         */
        QJsonObject rrd_files = event.value("rrdFiles").toObject();

        /*
         * Get graph config (common to all rrd indexes)
         */
        QJsonObject js_graphs = this->rrd_config.value("graphs").toObject();

        /*
         * Get graphs key and sort them
         */
        QStringList keys = js_graphs.keys();
        keys.sort();



        /*
         * Foreach rrdfiles
         */
        int row = 0;
        QStringListIterator i(rrd_files.keys());
        while (i.hasNext())
        {
            QString rrd_id = i.next();
            QString rrd_db_file = rrd_files.value(rrd_id).toString();

            /*
             * Each id is made by a frame and X number of graph columns.
             * The frame is then added to "frame" rows.
             */
            NFrame* fr = new NFrame(frame);
            NGrid*  gr = new NGrid();
            fr->setLayout(gr);



            /*
             * Set rrd_id as the QLabel for the first column
             */
            QLabel* desc_label = new QLabel(rrd_id, fr);
            gr->addWidget(desc_label, 0,0);


            /*
             * Initialize iterator.
             */
            QStringListIterator j(keys);


            /*
             * initialize grid column
             */
            int col = 1; // 0 used by "desc_label"
            while (j.hasNext())
            {
                    QString key = j.next();

                    /*
                     * From there, the Rrd4QtGraph() will handle himself showing
                     * the graph defined.
                     */
                    Rrd4QtGraph* graph = new Rrd4QtGraph(
                                rrd_db_file,                     // rrd db
                                js_graphs.value(key).toObject(), // graph def
                                fr);                             // parent

                    graph->setFixedHeight(300);

                    qDebug() << "add col: " << col;
                    gr->addWidget(graph, 0, col);

                    ++col;
            }
            grid->addWidget(fr, row, 0);
            ++row;
        }

        /*
         * Set the scroll area newly created widget
         */
        this->scroll_area->setWidget(frame);

        /*
         * From the "QScrollArea.setWidget(QWidget)" doc, added widget must
         * explicitely be show().
         */
        qDebug() << "table draw " << event;
        frame->show();

        return;
    }
}


void ProbeWindow::closeEvent(QCloseEvent* event)
{
    event->accept();
    this->deleteLater();
}


/*
 * STATIC
 */
void ProbeWindow::openWindow(QString name)
{
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
     * Raise, set focus and show in first Z order.
     */
    win->showNormal();
    win->setFocus();
    qApp->setActiveWindow(win);
}
