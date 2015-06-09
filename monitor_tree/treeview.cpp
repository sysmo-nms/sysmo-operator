#include "treeview.h"

TreeView::TreeView(QWidget* parent) : QTreeView(parent)
{
    this->setItemsExpandable(true);
    this->setRootIsDecorated(false);
    this->setWordWrap(true);
    this->setVerticalScrollMode(QAbstractItemView::ScrollPerPixel);
    this->setSelectionMode(QAbstractItemView::SingleSelection);
    //this->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    this->setEditTriggers(QAbstractItemView::NoEditTriggers);
    this->setContextMenuPolicy(Qt::CustomContextMenu);
    this->setObjectName("MonitorTreeView");
    this->setIconSize(QSize(22,22));
    this->setAnimated(true);
    this->setAlternatingRowColors(true);
    this->setAllColumnsShowFocus(false);
    this->setSortingEnabled(true);
    this->setExpandsOnDoubleClick(false);

    TreeModel* model = new TreeModel(this);
    this->filter_model = new QSortFilterProxyModel(this);
    this->filter_model->setSourceModel(model);
    this->filter_model->setDynamicSortFilter(true);
    this->filter_model->setFilterCaseSensitivity(Qt::CaseInsensitive);
    this->filter_model->setFilterRole(Sysmo::ROLE_FILTER_STRING);
    this->setModel(this->filter_model);

    this->timer = new QTimer(this);
    this->timer->setInterval(1000);
    this->timer->setSingleShot(false);
    this->timer->start();
    TreeDelegateProgress* progress = new TreeDelegateProgress(this);

    QObject::connect(
                model, SIGNAL(expandIndex(QModelIndex)),
                this,  SLOT(expandIndex(QModelIndex)));
    /*
     * connect delegate first
     */
    QObject::connect(
                this->timer, SIGNAL(timeout()),
                progress,    SLOT(ticTimeout()));

    QObject::connect(
                this->timer,      SIGNAL(timeout()),
                this->viewport(), SLOT(update()));

    this->setItemDelegateForColumn(2, progress);

    QFile file(":/tree/tree.qss");
    file.open(QIODevice::ReadOnly | QIODevice::Text);
    this->setStyleSheet(file.readAll());
    file.close();
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
