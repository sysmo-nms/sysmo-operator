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
#include "newprobepage1.h"


NewProbePage1::NewProbePage1(QString forTarget, QWizard* parent)
    : QWizardPage(parent)
{

    QMap<QString,QVariant> target = Monitor::getTarget(forTarget).toMap();

    QMap<QString,QVariant> properties = target.value("properties").toMap();
    QString snmpAwareStr = properties.value("isSnmpAware").toString();

    bool snmpAware;
    if (snmpAwareStr == "true") {
        snmpAware = true;
    } else {
        snmpAware = false;
    }

    qDebug() << "target is snmpAware" << snmpAware;

    this->setTitle("Select a probe");
    this->setSubTitle("User this form to add a probe to the target");

    /*
     * Result hiden. only here for register field
     */
    this->selection = new LineEdit(this);
    this->selection->hide();
    this->registerField("selection", this->selection);

    NGrid* grid = new NGrid();
    this->setLayout(grid);

    LineEdit* search = new LineEdit(this);
    search->setPlaceholderText("Filter");

    QPushButton* clear = new QPushButton(this);
    clear->setIcon(QIcon(":/icons/edit-clear.png"));

    QObject::connect(
                clear,  SIGNAL(clicked(bool)),
                search, SLOT(clear()));

    this->treeview = new QTreeView(this);
    this->treeview->setSelectionMode(QAbstractItemView::SingleSelection);
    this->treeview->setSortingEnabled(true);

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

    QPushButton * nchecks_help = new QPushButton(this);
    nchecks_help->setText("Developping a new extension...");
    nchecks_help->setIcon(QIcon(":/icons/help-browser.png"));
    nchecks_help->setFlat(true);
    QObject::connect(
                nchecks_help, SIGNAL(clicked(bool)),
                this,         SLOT(handleHelpTriggered()));

    grid->addWidget(clear, 0,0);
    grid->addWidget(search, 0,1);
    grid->addWidget(nchecks_help, 0,3);
    grid->addWidget(this->treeview, 1,0,1,5);
    grid->setColumnStretch(0,0);
    grid->setColumnStretch(1,1);
    grid->setColumnStretch(2,1);
    grid->setColumnStretch(3,0);
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
        ParseCheckGetInfos* parser = new ParseCheckGetInfos();
        reader.setContentHandler(parser);
        reader.setErrorHandler(parser);
        reader.parse(input);

        QStandardItem* item_name = new QStandardItem();
        item_name->setFlags(Qt::ItemIsSelectable|Qt::ItemIsEnabled);
        item_name->setData(parser->name, Qt::DisplayRole);

        QStandardItem* item_req = new QStandardItem();
        item_req->setFlags(Qt::ItemIsSelectable|Qt::ItemIsEnabled);
        item_req->setData(parser->require, Qt::DisplayRole);

        QStandardItem* item_desc = new QStandardItem();
        item_desc->setFlags(Qt::ItemIsSelectable|Qt::ItemIsEnabled);
        item_desc->setData(parser->desc, Qt::DisplayRole);

        QList<QStandardItem*> row;
        row.append(item_name);
        row.append(item_req);
        row.append(item_desc);
        model->appendRow(row);
        if (parser->require == "snmp" && !snmpAware) {
            item_name->setEnabled(false);
            item_name->setSelectable(false);
            item_req->setEnabled(false);
            item_req->setSelectable(false);
            item_desc->setEnabled(false);
            item_desc->setSelectable(false);
        }
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


void NewProbePage1::handleHelpTriggered()
{

    QDesktopServices::openUrl(QUrl("https://github.com/sysmo-nms/sysmo-nms.github.io/wiki/Sysmo-NChecks"));

}
