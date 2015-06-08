#include "treeview.h"

TreeView::TreeView(QWidget* parent) : QTreeView(parent)
{
    this->setItemsExpandable(true);
    this->setRootIsDecorated(true);
    this->setWordWrap(true);
    this->setVerticalScrollMode(QAbstractItemView::ScrollPerPixel);
    this->setSelectionMode(QAbstractItemView::SingleSelection);
    this->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    this->setEditTriggers(QAbstractItemView::NoEditTriggers);
    this->setContextMenuPolicy(Qt::CustomContextMenu);
    this->setObjectName("MonitorTreeView");
    this->setIconSize(QSize(22,22));
    this->setAnimated(true);
    this->setAlternatingRowColors(true);
    this->setAllColumnsShowFocus(false);
    this->setSortingEnabled(true);
    this->setExpandsOnDoubleClick(false);
    this->setModel(new TreeModel(this));

    this->timer = new QTimer(this);
    this->timer->setInterval(1000);
    this->timer->setSingleShot(false);
    this->timer->start();
    TreeDelegateProgress* progress = new TreeDelegateProgress(this);

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

    /*
    QString style;
    style.append("QTreeView::item:hover {");
    style.append("    font: bold 14px;");
    style.append("    border: 0px;");
    style.append("}");

    this->setStyleSheet(style);
    */
}


TreeView::~TreeView()
{
    /*
     * save state
     */
}


void TreeView::stopTimer() { this->timer->stop(); }
