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
    this->setIconSize(QSize(24,24));
    this->setAnimated(false);
    this->setAlternatingRowColors(true);
    this->setSortingEnabled(true);
    this->setModel(new TreeModel(this));
    this->setItemDelegateForColumn(1, new TreeDelegateProgress(this));
}


TreeView::~TreeView()
{
    /*
     * save state
     */
}
