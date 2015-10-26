#include "probewindow.h"

QHash<QString,ProbeWindow*> ProbeWindow::windows = QHash<QString,ProbeWindow*>();

ProbeWindow::ProbeWindow(QString probeName)
                        : MonitorProxyWidget(probeName)
{
    this->divider = 1;
    this->margin = 150;
    this->name = probeName;

    /*
     * Init various element of QWidget. The newly created window is non
     * modal and will cleanly close on application shutdown.
     */
    this->setWindowFlags(this->windowFlags() | Qt::Window);
    this->setWindowModality(Qt::NonModal);
    this->setAttribute(Qt::WA_QuitOnClose, false);


    /*
     * Get the check identifier and target belong_to
     */
    Monitor*      mon = Monitor::getInstance();
    QJsonObject probe = mon->probes->value(this->name);
    QString  probe_id = probe.value("probeId").toString();
    QString belong_to = probe.value("target").toString();
    this->target = mon->targets->value(belong_to);

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
     * Init QTimer for graph width
     */
    this->timer = new QTimer(this);
    this->timer->setSingleShot(true);
    this->timer->setInterval(500);
    QObject::connect(
                this->timer, SIGNAL(timeout()),
                this, SLOT(handleTimerTimeout()));

    /*
     * begin generic layout
     */
    // top log area controls
    NFrame* log_controls = new NFrame(this);
    NGridContainer* lc_grid = new NGridContainer();
    log_controls->setLayout(lc_grid);

    QLabel* time_line_label = new QLabel("TimeLine:", this);
    NoWheelComboBox* time_span_cbox  = new NoWheelComboBox(this);
    time_span_cbox->insertItem(ProbeWindow::SPAN_TWO_HOURS,    "2h from now");
    time_span_cbox->insertItem(ProbeWindow::SPAN_TWELVE_HOURS, "12h from now");
    time_span_cbox->insertItem(ProbeWindow::SPAN_TWO_DAYS,     "2d from now");
    time_span_cbox->insertItem(ProbeWindow::SPAN_SEVEN_DAYS,   "7d from now");
    time_span_cbox->insertItem(ProbeWindow::SPAN_TWO_WEEKS,    "2w from now");
    time_span_cbox->insertItem(ProbeWindow::SPAN_ONE_MONTH,    "1m from now");
    time_span_cbox->insertItem(ProbeWindow::SPAN_SIX_MONTH,    "6m from now");
    time_span_cbox->insertItem(ProbeWindow::SPAN_ONE_YEAR,     "1y from now");
    time_span_cbox->insertItem(ProbeWindow::SPAN_THREE_YEARS,  "3y from now");
    time_span_cbox->insertItem(ProbeWindow::SPAN_TEN_YEARS,    "10y from now");
    time_span_cbox->setCurrentIndex(ProbeWindow::SPAN_SEVEN_DAYS);
    QObject::connect(
                time_span_cbox, SIGNAL(currentIndexChanged(int)),
                this,           SLOT(handleSpanChanged(int)));
    lc_grid->addWidget(time_line_label, 0,0);
    lc_grid->addWidget(time_span_cbox, 0,1);

    QLabel* height_label = new QLabel("Graph height:", this);
    this->height_cbox  = new NoWheelComboBox(this);
    this->height_cbox->insertItem(ProbeWindow::HEIGHT_SMALL,     "Small");
    this->height_cbox->insertItem(ProbeWindow::HEIGHT_NORMAL,    "Normal");
    this->height_cbox->insertItem(ProbeWindow::HEIGHT_LARGE,     "Large");
    this->height_cbox->setCurrentIndex(ProbeWindow::HEIGHT_NORMAL);
    QObject::connect(
                this->height_cbox, SIGNAL(currentIndexChanged(int)),
                this,              SLOT(handleHeightChanged(int)));
    lc_grid->addWidget(height_label, 0,2);
    lc_grid->addWidget(this->height_cbox, 0,3);

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
    this->restoreStateFromSettings();
}

ProbeWindow::~ProbeWindow()
{
    ProbeWindow::windows.remove(this->name);

    QString geom_str  = "win_geometry/" + this->name;
    QSettings s;
    s.setValue(geom_str, this->saveGeometry());

    QString size_str = "graph_size/" + this->name;
    s.setValue(size_str, QVariant(this->height_cbox->currentIndex()));
}

void ProbeWindow::restoreStateFromSettings()
{
    QString geom_str  = "win_geometry/" + this->name;
    QSettings s;
    QVariant geom_var = s.value(geom_str);
    if (geom_var.isValid()) {
        this->restoreGeometry(geom_var.toByteArray());
    } else {
        this->setGeometry(0,0,900,500);
    }

    QString size_str = "graph_size/" + this->name;
    QVariant size_var = s.value(size_str);
    if(size_var.isValid()) {
        this->height_cbox->setCurrentIndex(size_var.toInt());
    }
}

void ProbeWindow::handleTimerTimeout()
{
    int margins = this->margin * this->divider;
    int size = (this->size().width() - margins) / this->divider;
    emit this->graphWidthChanged(size);
}

void ProbeWindow::resizeEvent(QResizeEvent *event)
{
    this->timer->start();
    MonitorProxyWidget::resizeEvent(event);
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
     * get initial height
     */
    int initial_height = this->getHeightFor(this->height_cbox->currentIndex());

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
                            initial_height,
                            frame);                            // parent

            QObject::connect(
                         this,  SIGNAL(graphWidthChanged(int)),
                         graph, SLOT(setGraphWidth(int)));

            QObject::connect(
                        this,  SIGNAL(timeSpanChanged(int)),
                        graph, SLOT(setTimeSpan(int)));

            QObject::connect(
                        this,  SIGNAL(graphHeightChanged(int)),
                        graph, SLOT(setGraphHeight(int)));


            grid->addWidget(graph, row, 0);
            grid->setRowStretch(row,0);

            ++row;
        }
        grid->setRowStretch(row,1);

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
        this->divider = keys.size();


        /*
         * Get prop suffix and prefix
         */
        QString prefix = this->rrd_config.value("propertyPrefix").toString();
        QString suffix = this->rrd_config.value("propertySuffix").toString();

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
            fr->setFrameShape(QFrame::StyledPanel);
            NGrid*  gr = new NGrid();
            fr->setLayout(gr);

            /*
             * Set rrd_id as the QLabel for the first column
             */
            QString prop_content = this->target.value("properties").toObject()
                         .value(prefix + rrd_id + suffix).toString("undefined");
            QString lab_text;
            if (prop_content == "undefined") {
                lab_text = "<h3>" + rrd_id + "</h3>";
            } else {
                lab_text = "<h3>" + prop_content + "</h3>";
            }
            QLabel* desc_label = new QLabel(lab_text, fr);
            desc_label->setFixedWidth(100);
            desc_label->setBackgroundRole(QPalette::Base);
            desc_label->setAutoFillBackground(true);
            desc_label->setAlignment(Qt::AlignCenter);
            gr->addWidget(desc_label, 0,0);
            gr->setColumnStretch(0,0);

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
                                initial_height,                  //initial height
                                fr);                             // parent

                    QObject::connect(
                         this,  SIGNAL(graphWidthChanged(int)),
                         graph, SLOT(setGraphWidth(int)));


                    QObject::connect(
                         this,  SIGNAL(timeSpanChanged(int)),
                         graph, SLOT(setTimeSpan(int)));

                    QObject::connect(
                         this,  SIGNAL(graphHeightChanged(int)),
                         graph, SLOT(setGraphHeight(int)));


                    qDebug() << "add col: " << col;
                    gr->addWidget(graph, 0, col);

                    ++col;
            }
            grid->setRowStretch(row, 0);
            grid->addWidget(fr, row, 0);
            ++row;
        }
        grid->setRowStretch(row, 1);

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
    ProbeWindow* win;

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

int ProbeWindow::getHeightFor(int value)
{
    switch (value)
    {
    case ProbeWindow::HEIGHT_SMALL:
        return 30;
    case ProbeWindow::HEIGHT_NORMAL:
        return 90;
    case ProbeWindow::HEIGHT_LARGE:
        return 180;
    default:
        qWarning() << "unknown size:" << value;
        return 150;
    }
}

int ProbeWindow::getSpanFor(int value)
{
    switch(value)
    {
    case ProbeWindow::SPAN_TWO_HOURS:
        return 7200;
    case ProbeWindow::SPAN_TWELVE_HOURS:
        return 43200;
    case ProbeWindow::SPAN_TWO_DAYS:
        return 172800;
    case ProbeWindow::SPAN_SEVEN_DAYS:
        return 604800;
    case ProbeWindow::SPAN_TWO_WEEKS:
        return 1209600;
    case ProbeWindow::SPAN_ONE_MONTH:
        return 2592000;
    case ProbeWindow::SPAN_SIX_MONTH:
        return 15552000;
    case ProbeWindow::SPAN_ONE_YEAR:
        return 31536000;
    case ProbeWindow::SPAN_THREE_YEARS:
        return 94608000;
    case ProbeWindow::SPAN_TEN_YEARS:
        return 315360000;
    default:
        qWarning() << "Unknown time span:" << value;
        return 604800;
    }
}

bool ProbeWindow::isThumbnail(int value)
{
    Q_UNUSED(value);
    /*
    switch(value)
    {
    case ProbeWindow::HEIGHT_THUMBNAIL:
        return true;
    default:
        return false;
    }
    */
    return false;
}

void ProbeWindow::handleHeightChanged(int height)
{
    int height_val = ProbeWindow::getHeightFor(height);
    emit this->graphHeightChanged(height_val);
}

void ProbeWindow::handleSpanChanged(int span)
{
    int span_val = ProbeWindow::getSpanFor(span);
    emit this->timeSpanChanged(span_val);
}
