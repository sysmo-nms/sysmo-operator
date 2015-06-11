#include "treeview.h"

TreeView::TreeView(QWidget* parent) : QTreeView(parent)
{
    this->setItemsExpandable(true);
    this->setRootIsDecorated(false);
    this->setWordWrap(true);
    this->setVerticalScrollMode(QAbstractItemView::ScrollPerPixel);
    this->setSelectionMode(QAbstractItemView::SingleSelection);
    this->setEditTriggers(QAbstractItemView::NoEditTriggers);
    this->setContextMenuPolicy(Qt::CustomContextMenu);
    QObject::connect(
                this, SIGNAL(customContextMenuRequested(QPoint)),
                this, SLOT(openContextMenu(QPoint)));
    this->setObjectName("MonitorTreeView");
    this->setIconSize(QSize(22,22));
    this->setAnimated(true);
    this->setAlternatingRowColors(true);
    this->setAllColumnsShowFocus(false);
    this->setSortingEnabled(true);
    this->setExpandsOnDoubleClick(false);

    this->original_model = new TreeModel(this);
    this->filter_model   = new QSortFilterProxyModel(this);
    this->filter_model->setSourceModel(this->original_model);
    this->filter_model->setDynamicSortFilter(true);
    this->filter_model->setFilterCaseSensitivity(Qt::CaseSensitive);
    this->filter_model->setFilterRole(Sysmo::ROLE_FILTER_STRING);
    this->setModel(this->filter_model);

    this->timer = new QTimer(this);
    this->timer->setInterval(1000);
    this->timer->setSingleShot(false);
    this->timer->start();
    DelegateProbeProgress* progress = new DelegateProbeProgress(this);

    QObject::connect(
                this->original_model, SIGNAL(expandIndex(QModelIndex)),
                this,                 SLOT(expandIndex(QModelIndex)));
    /*
     * connect delegate first
     */
    QObject::connect(
                this->timer, SIGNAL(timeout()),
                progress,    SLOT(ticTimeout()));

    QObject::connect(
                this->timer,      SIGNAL(timeout()),
                this->viewport(), SLOT(update()));

    this->setItemDelegateForColumn(3, progress);

    QFile file(":/tree/tree.qss");
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    this->setStyleSheet(file.readAll());
    file.close();

    /*
     * Acceptable defaults. Overriden by restore state.
     */
    this->setColumnWidth(0, 250);
    this->setColumnWidth(1, 65);
    this->setColumnWidth(2, 65);
    this->setColumnWidth(3, 100);

    // TODO restore state
}


TreeView::~TreeView()
{
    /*
     * save state
     */
}


// SLOTS
void TreeView::expandIndex(QModelIndex index)
{
    this->expand(this->filter_model->mapFromSource(index));
}

void TreeView::stopTimer() { this->timer->stop(); }

void TreeView::openContextMenu(const QPoint point) {
    QModelIndex    index = this->filter_model->mapToSource(this->indexAt(point));
    QStandardItem* item  = this->original_model->itemFromIndex(index);
    if (item->type() == Sysmo::TYPE_PROBE) {
        QString element_name = item->data(Sysmo::ROLE_ELEMENT_NAME).toString();
        QJsonObject val = Monitor::probe_map->value(element_name);
        qDebug() << "probe name: " << element_name << val;
    } else if (item->type() == Sysmo::TYPE_TARGET) {
        QString element_name = item->data(Sysmo::ROLE_ELEMENT_NAME).toString();
        QJsonObject val = Monitor::target_map->value(element_name);
        qDebug() << "target name: " << element_name << val;
    }
}
