#include "treeview.h"

TreeView::TreeView(QWidget* parent) : QTreeView(parent)
{
    this->setItemsExpandable(true);
    this->setRootIsDecorated(false);
    this->setWordWrap(true);
    this->setVerticalScrollMode(QAbstractItemView::ScrollPerPixel);
    this->setSelectionMode(QAbstractItemView::SingleSelection);
    this->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    this->setEditTriggers(QAbstractItemView::NoEditTriggers);
    this->setContextMenuPolicy(Qt::CustomContextMenu);
    this->setObjectName("MonitorTreeView");
    this->setIconSize(QSize(22,22));
    this->setAnimated(false);
    this->setAlternatingRowColors(true);
    this->setSortingEnabled(true);
    this->setModel(new TreeModel(this));

    QTimer* timer = new QTimer(this);
    timer->setInterval(1000);
    timer->setSingleShot(false);
    timer->start();
    TreeDelegateProgress* progress = new TreeDelegateProgress(this);

    /*
     * connect delegate first
     */
    QObject::connect(
                timer,    SIGNAL(timeout()),
                progress, SLOT(ticTimeout()));

    QObject::connect(
                timer,            SIGNAL(timeout()),
                this->viewport(), SLOT(update()));

    this->setItemDelegateForColumn(2, progress);
}

TreeView::~TreeView()
{
    /*
     * save state
     */
}
