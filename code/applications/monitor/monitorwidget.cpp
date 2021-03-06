/*
Sysmo NMS Network Management and Monitoring solution (https://sysmo-nms.github.io)

Copyright (c) 2012-2017 Sebastien Serre <ssbx@sysmo.io>

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
#include "monitorwidget.h"

#include <widgets/nframe.h>
#include <widgets/ngrid.h>
#include <widgets/ngridcontainer.h>
#include <widgets/statusbuttonwidget.h>
#include <widgets/lineedit.h>
#include <network/supercast.h>
#include <network/supercastsignal.h>

#include "treeview.h"
#include "nchecks.h"
#include "monitorlogs.h"
#include "dialogs/newtarget.h"

#include <QObject>
#include <QLabel>
#include <QFrame>
#include <QPushButton>
#include <QIcon>
#include <QMap>
#include <QDesktopServices>
#include <QUrl>
#include <QPalette>
#include <QPixmap>
#include <QSettings>
#include <QVariant>

#include <QDebug>


MonitorWidget* MonitorWidget::singleton = NULL;

MonitorWidget* MonitorWidget::getInstance() {
    return MonitorWidget::singleton;
}

MonitorWidget::MonitorWidget(QWidget* parent) : QSplitter(parent) {

    MonitorWidget::singleton = this;

    this->setContentsMargins(0,0,0,0);
    /*
     * Initialize utils first
     */
    this->mon = new Monitor(this);
    new NChecks(this);


    /*
     * init layout
     */

    // timeline panel
    NFrame* timelineFrame = new NFrame(this);
    timelineFrame->setMinimumWidth(150);
    NGrid* tgrid = new NGrid();
    timelineFrame->setLayout(tgrid);
    timelineFrame->setFrameShape(QFrame::StyledPanel);

    MonitorLogs* timeline = new MonitorLogs(this);
    tgrid->addWidget(timeline, 0, 1);
    //tgrid->addWidget(statusBox, 0,0);
    tgrid->setColumnStretch(0, 0);
    tgrid->setColumnStretch(1, 1);

    // tree frame
    NFrame* treeFrame = new NFrame(this);
    treeFrame->setMinimumWidth(150);
    treeFrame->setFrameShape(QFrame::StyledPanel);
    NGrid* treegrid = new NGrid();
    treegrid->setVerticalSpacing(4);
    treeFrame->setLayout(treegrid);

    this->setOrientation(Qt::Vertical);
    this->addWidget(treeFrame);
    this->addWidget(timelineFrame);

    /*
     * top controls
     */
    QPushButton* create = new QPushButton(this);
    create->setIcon(QIcon(":/icons/list-add.png"));
    create->setStatusTip("Create a new target.");
    QObject::connect(
            create, SIGNAL(clicked(bool)),
            this, SLOT(showNewTargetDialog()));

    QPushButton* clear = new QPushButton(this);
    clear->setIcon(QIcon(":/icons/edit-clear.png"));
    clear->setStatusTip("Clear filter line");

    LineEdit* search = new LineEdit(this);
    search->setFixedWidth(250);
    search->setStatusTip("Filter the target/probe view");
    QObject::connect(
            clear, SIGNAL(pressed()),
            search, SLOT(clear()));

    StatusButtonWidget* statusBox = new StatusButtonWidget(this);
    QObject::connect(
            statusBox->err, SIGNAL(setText(QString)),
            search, SLOT(setText(QString)));
    QObject::connect(
            statusBox->crit, SIGNAL(setText(QString)),
            search, SLOT(setText(QString)));
    QObject::connect(
            statusBox->warn, SIGNAL(setText(QString)),
            search, SLOT(setText(QString)));


    // clear/search layout
    NFrameContainer* search_clear = new NFrameContainer(this);
    NGridContainer* search_clear_grid = new NGridContainer();
    search_clear->setLayout(search_clear_grid);
    search_clear_grid->addWidget(clear, 0, 0);
    search_clear_grid->addWidget(search, 0, 1);
    search_clear_grid->addWidget(statusBox, 0, 2);
    search_clear_grid->setColumnStretch(0, 0);
    search_clear_grid->setColumnStretch(1, 1);
    search_clear_grid->setHorizontalSpacing(4);

    // help button
    QPushButton* help = new QPushButton(this);
    help->setIcon(QIcon(":/icons/help-browser.png"));
    help->setFlat(true);
    help->setToolTip("Get help...");
    QObject::connect(
            help, SIGNAL(clicked(bool)),
            this, SLOT(handleHelpClicked()));


    /*
     * treeview
     */
    TreeView* tree = new TreeView(this);

    QObject::connect(
            clear, SIGNAL(clicked(bool)),
            tree, SLOT(clearSelection()));
    QObject::connect(
            search, SIGNAL(textChanged(QString)),
            tree->filter_model, SLOT(setFilterFixedString(QString)));
    QObject::connect(
            search, SIGNAL(textChanged(QString)),
            tree, SLOT(expandAll()));
    QObject::connect(
            tree->add_target_action, SIGNAL(triggered(bool)),
            this, SLOT(showNewTargetDialog()));
    QObject::connect(
            this->mon, SIGNAL(initialSyncEnd()),
            tree, SLOT(initialSyncEnd()));

    // new probe dialog connect
    QObject::connect(
            tree->target_menu, SIGNAL(openNewProbeDialog(QString)),
            this, SLOT(showNewProbeDialog(QString)));


    /*
     * right layout
     */
    treegrid->addWidget(create, 0, 0);
    treegrid->addWidget(search_clear, 0, 1);
    treegrid->addWidget(help, 0, 3);
    treegrid->addWidget(tree, 1, 0, 1, 4);
    treegrid->setColumnStretch(0, 0);
    treegrid->setColumnStretch(1, 0);
    treegrid->setColumnStretch(2, 3);
    treegrid->setRowStretch(0, 0);
    treegrid->setRowStretch(1, 1);
    this->restoreStateFromSettings();

}

MonitorWidget::~MonitorWidget() {
    QSettings s;
    s.setValue("monitor/splitter_state", this->saveState());
}

void
MonitorWidget::restoreStateFromSettings() {
    QSettings s;
    QVariant splitter_state = s.value("monitor/splitter_state");
    if (splitter_state.isValid()) {
        this->restoreState(splitter_state.toByteArray());
    }
}

void MonitorWidget::connectionStatus(int status) {

    if (status == Supercast::CONNECTION_SUCCESS) {
        SupercastSignal* sig = new SupercastSignal();
        QObject::connect(
                sig, SIGNAL(serverMessage(QVariant)),
                this->mon, SLOT(handleServerMessage(QVariant)));

        Supercast::subscribe("monitor_main", sig);
    } else {
        // the application is in an error state.
        TreeView* tree = this->findChild<TreeView *>("MonitorTreeView");
        tree->stopTimer();
    }

}

/*
 * Dialogs will open at the center of the application when launched
 * from a central widget, wich is the case for MonitorWidget.
 */
void MonitorWidget::showNewTargetDialog() {

    NewTarget* tdial = new NewTarget(this);
    tdial->exec();
    tdial->deleteLater();

}

void MonitorWidget::showNewProbeDialog(QString forTarget) {

    NewProbe* pdial = new NewProbe(forTarget, this);
    pdial->exec();
    pdial->deleteLater();

}

void MonitorWidget::handleHelpClicked() {

    QDesktopServices::openUrl(QUrl("https://sysmo-nms.github.io/Community/"));

}
