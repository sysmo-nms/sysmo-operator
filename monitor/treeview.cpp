#include "treeview.h"

TreeView::TreeView(QWidget* parent) : QTreeView(parent)
{
    this->target_menu = new MenuTarget(this);
    this->probe_menu  = new MenuProbe(this);
    QObject::connect(
                this,   SIGNAL(doubleClicked(QModelIndex)),
                this,   SLOT(handleDoubleClicked(QModelIndex)));
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

    /*
     * Set stylesheet mainly for custom branch draw
     */
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
     * TODO save state
     */
}


// SLOTS
void TreeView::expandIndex(QModelIndex index)
{
    this->expand(this->filter_model->mapFromSource(index));
}

void TreeView::stopTimer() { this->timer->stop(); }

void TreeView::openContextMenu(const QPoint point) {

    QModelIndex    index   = this->filter_model->mapToSource(this->indexAt(point));
    QModelIndex    element = index.sibling(index.row(), 0);
    QStandardItem* item    = this->original_model->itemFromIndex(element);

    if (item->type() == Sysmo::TYPE_PROBE)
    {
        QString probe = item->data(Sysmo::ROLE_ELEMENT_NAME).toString();
        this->probe_menu->showMenuFor(probe, this->mapToGlobal(point));
    }
    else if(item->type() == Sysmo::TYPE_TARGET)
    {
        QString target = item->data(Sysmo::ROLE_ELEMENT_NAME).toString();
        this->target_menu->showMenuFor(target, this->mapToGlobal(point));
    }
}

void TreeView::handleDoubleClicked(const QModelIndex index)
{
    QModelIndex idx_sibling = index.sibling(index.row(), 0);
    QModelIndex idx_origin  = this->filter_model->mapToSource(idx_sibling);
    QStandardItem*     item = this->original_model->itemFromIndex(idx_origin);

    QString name = item->data(Sysmo::ROLE_ELEMENT_NAME).toString();
    if (item->type() == Sysmo::TYPE_PROBE)
    {
        ProbeWindow::openWindow(name);
    }
    else if (item->type() == Sysmo::TYPE_TARGET)
    {
        MonitorActions::openActionFor(name);
    }
}
