/*
Sysmo NMS Network Management and Monitoring solution (http://www.sysmo.io)

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
#ifndef NEWPROBEPAGE1_H
#define NEWPROBEPAGE1_H
#include <QWizardPage>
#include <QString>
#include <QWizard>
#include <QTreeView>
#include "lineedit.h"

class NewProbePage1 : public QWizardPage {
    Q_OBJECT

public:
    /*
     * QWizard parent for connecting to QWizard::next()
     */
    NewProbePage1(QString forTarget, QWizard* parent = 0);
    bool isComplete() const;
    int nextId() const;

private:
    QTreeView* treeview;
    LineEdit* selection;

private slots:
    void handleHelpTriggered();
};

#endif // NEWPROBEPAGE1_H
