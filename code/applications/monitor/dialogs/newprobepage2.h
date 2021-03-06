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
#ifndef NEWPROBEPAGE2_H
#define NEWPROBEPAGE2_H
#include <widgets/lineedit.h>
#include <widgets/nframe.h>
#include <widgets/ngrid.h>

#include <QWizard>
#include <QWizardPage>
#include <QString>
#include <QMap>
#include <QTextEdit>
#include <QList>
#include <QWidget>
#include <QObject>
#include <QProgressDialog>
#include <QVariant>
#include <QDialog>
#include <QTreeWidgetItem>

class NewProbePage2 : public QWizardPage {
    Q_OBJECT
public:
    NewProbePage2(QString forTarget, QWizard* parent = 0);
    void initializePage();
    void cleanupPage();
    bool validatePage();
    bool isComplete() const;
    int nextId() const;

private:
    QString target;
    QString probe_class;
    QMap<QString, LineEdit*>* args;
    QTextEdit* docs;
    NFrame* form_frame;
    NGrid* grid;
    LineEdit *name_line;
    QList<LineEdit*>* mandatory_args;
};

class HelperExec : public QObject {
    Q_OBJECT
public:
    HelperExec(LineEdit* line, QWidget *parent = 0);
    QString h_class;
    QString h_target;
    QWidget* w_parent;
    LineEdit* flag_line;

private:
    QProgressDialog* dial;

public slots:
    void execHelper();

private slots:
    void helperReply(QVariant reply);
};

class HelperDialog : public QDialog {
    Q_OBJECT
public:
    HelperDialog(QVariant helperReply, QWidget* parent = 0);
    QString getValue();

private:
    QString value;
    QString list_separator;
    QMap<QString, QTreeWidgetItem*> root_items;

public slots:
    void refreshTreeState(QTreeWidgetItem* item, int column);
    void resetTreeCheckState();
    void validateSelection();
};

#endif // NEWPROBEPAGE2_H
