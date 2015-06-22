#include "newprobepage1.h"

NewProbePage1::NewProbePage1(QWizard* parent) : QWizardPage(parent)
{
    this->setTitle("Select a probe");
    this->setSubTitle("User this form to add a probe to the target");

    /*
     * Result hiden. only here for register field
     */
    this->selection = new QLineEdit(this);
    this->selection->hide();
    this->registerField("selection", this->selection);

    NGrid* grid = new NGrid();
    this->setLayout(grid);

    QLineEdit* search = new QLineEdit(this);
    search->setPlaceholderText("Filter");

    QPushButton* clear = new QPushButton(this);
    clear->setIcon(QIcon(":/icons/edit-clear.png"));

    QObject::connect(
                clear,  SIGNAL(clicked(bool)),
                search, SLOT(clear()));

    this->treeview = new QTreeView(this);
    this->treeview->setSelectionMode(QAbstractItemView::SingleSelection);

    QObject::connect(
                this->treeview, SIGNAL(clicked(QModelIndex)),
                this,           SIGNAL(completeChanged()));

    QObject::connect(
                clear,          SIGNAL(clicked(bool)),
                this->treeview, SLOT(clearSelection()));

    QObject::connect(
                clear, SIGNAL(clicked(bool)),
                this,  SIGNAL(completeChanged()));

    QObject::connect(
                this->treeview, SIGNAL(doubleClicked(QModelIndex)),
                parent,         SLOT(next()));

    QStandardItemModel* model = new QStandardItemModel(this);
    model->setColumnCount(2);
    QStringList headers;
    headers << "Class" << "Type" << "Description";
    model->setHorizontalHeaderLabels(headers);

    QSortFilterProxyModel* proxy = new QSortFilterProxyModel(this);
    proxy->setFilterCaseSensitivity(Qt::CaseInsensitive);
    proxy->setDynamicSortFilter(true);
    proxy->setFilterRole(Qt::DisplayRole);
    proxy->setSourceModel(model);
    proxy->setFilterKeyColumn(-1);

    QObject::connect(
                search, SIGNAL(textChanged(QString)),
                proxy,  SLOT(setFilterFixedString(QString)));

    QObject::connect(
                search, SIGNAL(textChanged(QString)),
                this,   SIGNAL(completeChanged()));

    this->treeview->setModel(proxy);

    grid->addWidget(clear, 0,0);
    grid->addWidget(search, 0,1);
    grid->addWidget(this->treeview, 1,0,1,3);
    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,1);
    grid->setColumnStretch(2,1);
    grid->setRowStretch(0,0);
    grid->setRowStretch(1,1);

    /*
     * Populate model
     */
    QList<QString> checks = NChecks::getCheckList();

    QXmlInputSource* input = new QXmlInputSource();
    QXmlSimpleReader reader;
    QList<QString>::iterator i;
    for (i = checks.begin(); i != checks.end(); ++i) {
        input->setData(NChecks::getCheck(*i));
        CheckDefParser* parser = new CheckDefParser();
        reader.setContentHandler(parser);
        reader.setErrorHandler(parser);
        reader.parse(input);

        QStandardItem* item_name = new QStandardItem();
        item_name->setFlags(Qt::ItemIsSelectable|Qt::ItemIsEnabled);
        item_name->setData(parser->name, Qt::DisplayRole);

        QStandardItem* item_type = new QStandardItem();
        item_type->setFlags(Qt::ItemIsSelectable|Qt::ItemIsEnabled);
        item_type->setData(parser->type, Qt::DisplayRole);

        QStandardItem* item_desc = new QStandardItem();
        item_desc->setFlags(Qt::ItemIsSelectable|Qt::ItemIsEnabled);
        item_desc->setData(parser->desc, Qt::DisplayRole);

        QList<QStandardItem*> row;
        row.append(item_name);
        row.append(item_type);
        row.append(item_desc);
        model->appendRow(row);
        delete parser;
    }
    delete input;
    this->treeview->resizeColumnToContents(0);
    this->treeview->resizeColumnToContents(1);
}

bool NewProbePage1::isComplete() const
{
    QList<QModelIndex> idx = this->treeview->selectionModel()->selectedIndexes();
    if (idx.length() == 0) {
        this->selection->setText("");
        return false;
    }

    QModelIndex id = idx.first();
    this->selection->setText(id.data().toString());
    qDebug() << "field is: " << this->field("selection");
    return true;
}


int NewProbePage1::nextId() const {return 2;}



/*
 * Check xml parser
 */
bool CheckDefParser::startElement(
        const QString &namespaceURI,
        const QString &localName,
        const QString &qName,
        const QXmlAttributes &atts)
{
    Q_UNUSED(namespaceURI);
    Q_UNUSED(localName);
    if (qName == "Check")
    {
        this->name = atts.value("Id");
        this->type = atts.value("Type");
    } else if (qName == "Description") {
        this->descIsNext = true;
    }
    return true;
}

bool CheckDefParser::characters(const QString &ch)
{
    if (this->descIsNext) {
        this->desc = ch;
        return false;
    }
    return true;
}
