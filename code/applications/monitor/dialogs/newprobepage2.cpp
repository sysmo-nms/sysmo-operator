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
#include "newprobepage2.h"
#include "newprobeprogressdialog.h"
#include <widgets/messagebox.h>

#include <sysmo.h>
#include <widgets/nframecontainer.h>
#include <widgets/ngridcontainer.h>
#include <applications/monitor/monitor.h>
#include <applications/monitor/nchecks.h>
#include <applications/monitor/xml/parsecheckmakedoc.h>
#include <applications/monitor/xml/parsecheckmakeform.h>
#include <network/supercastsignal.h>
#include <network/supercast.h>
#include <network/qjson.h>


#include <QFormLayout>
#include <QPushButton>
#include <QStringList>
#include <QList>
#include <QLabel>
#include <QXmlInputSource>
#include <QXmlSimpleReader>
#include <QTreeWidget>
#include <QAbstractItemView>
#include <QHeaderView>
#include <QDialogButtonBox>
#include <QPushButton>

#include <QDebug>

NewProbePage2::NewProbePage2(
        QString forTarget,
        QWizard* parent) : QWizardPage(parent) {

    this->target = forTarget;
    this->probe_class = "";
    this->setSubTitle("Complete the form to configure the new probe");
    this->setFinalPage(true);
    this->grid = new NGrid();
    this->setLayout(grid);

    this->docs = new QTextEdit(this);
    this->docs->setReadOnly(true);
    this->grid->addWidget(this->docs, 0, 1);
    this->grid->setColumnStretch(0, 1);
    this->grid->setColumnStretch(1, 1);

}

int NewProbePage2::nextId() const {

    return -1;

}

void NewProbePage2::cleanupPage() {

    this->grid->removeWidget(this->form_frame);
    this->form_frame->deleteLater();
    delete this->args;
    delete this->mandatory_args;

}

void NewProbePage2::initializePage() {

    this->form_frame = new NFrame(this);
    this->grid->addWidget(this->form_frame, 0, 0);
    this->args = new QMap<QString, LineEdit*>();
    this->mandatory_args = new QList<LineEdit*>();

    QString str("Configure probe %1");
    QString probe_name(this->field("selection").toString());
    this->setTitle(str.arg(probe_name));

    QXmlSimpleReader reader;
    /*
     * Generate documentation
     */
    QXmlInputSource* doc_input = new QXmlInputSource();
    doc_input->setData(NChecks::getCheck(probe_name));
    ParseCheckMakeDoc* doc_parser = new ParseCheckMakeDoc();
    reader.setContentHandler(doc_parser);
    reader.setErrorHandler(doc_parser);
    reader.parse(doc_input);
    this->docs->setHtml(doc_parser->doc);
    delete doc_parser;
    delete doc_input;


    /*
     * Generate form
     */
    QXmlInputSource* form_input = new QXmlInputSource();
    form_input->setData(NChecks::getCheck(probe_name));
    ParseCheckMakeForm* form_parser = new ParseCheckMakeForm();
    reader.setContentHandler(form_parser);
    reader.setErrorHandler(form_parser);
    reader.parse(form_input);

    this->probe_class = form_parser->probe_class;


    this->name_line = new LineEdit(this);
    this->name_line->setText(probe_name);

    QFormLayout* form = new QFormLayout();
    this->form_frame->setLayout(form);

    NFrame* separator0 = new NFrame(this->form_frame);
    separator0->setFixedHeight(30);
    form->addRow("Display name", this->name_line);
    form->addRow(separator0);

    QList<FormConfig>* mandat = form_parser->mandatory;
    QList<FormConfig>::iterator i;
    for (i = mandat->begin(); i != mandat->end(); ++i) {
        qDebug() << "iterate" << i->flag_name;
        LineEdit* edit = new LineEdit(this->form_frame);
        this->args->insert(i->flag_name, edit);
        this->mandatory_args->append(edit);
        QObject::connect(
                edit, SIGNAL(textChanged(QString)),
                this, SIGNAL(completeChanged()));

        edit->setPlaceholderText(i->hint);
        edit->setToolTip(i->hint);
        if (i->has_helper) {
            NFrameContainer* fr = new NFrameContainer(this->form_frame);
            NGridContainer* gr = new NGridContainer(fr);
            QPushButton* hbut = new QPushButton(this->form_frame);
            hbut->setIcon(QIcon(":/icons/help-browser.png"));
            hbut->setToolTip(i->helper_descr);
            HelperExec* ex = new HelperExec(edit, this->form_frame);
            ex->h_class = i->helper_class;
            ex->h_target = this->target;
            QObject::connect(
                    hbut, SIGNAL(clicked(bool)),
                    ex, SLOT(execHelper()));

            gr->addWidget(edit, 0, 0);
            gr->addWidget(hbut, 0, 1);
            gr->setColumnStretch(0, 1);
            gr->setColumnStretch(1, 0);
            form->addRow(i->flag_name, fr);
        } else {
            form->addRow(i->flag_name, edit);
        }
    }

    NFrame* separator = new NFrame(this->form_frame);
    separator->setFixedHeight(20);
    form->addRow(separator);

    QList<FormConfig>* options = form_parser->options;
    QList<FormConfig>::iterator j;
    for (j = options->begin(); j != options->end(); ++j) {
        LineEdit* edit = new LineEdit(this->form_frame);
        this->args->insert(j->flag_name, edit);
        edit->setPlaceholderText(j->hint);
        edit->setText(j->defaults);
        edit->setToolTip(j->hint);
        if (j->has_helper) {
            qDebug() << "had helper";
            NFrameContainer* fr = new NFrameContainer(this->form_frame);
            NGridContainer* gr = new NGridContainer(fr);

            QPushButton* hbut = new QPushButton(this->form_frame);
            HelperExec* ex = new HelperExec(edit, this->form_frame);
            ex->h_class = j->helper_class;
            ex->h_target = this->target;
            QObject::connect(
                    hbut, SIGNAL(clicked(bool)),
                    ex, SLOT(execHelper()));
            gr->addWidget(edit, 0, 0);
            gr->addWidget(hbut, 0, 1);
            gr->setColumnStretch(0, 1);
            gr->setColumnStretch(1, 0);
            form->addRow(j->flag_name, fr);
        } else {
            form->addRow(j->flag_name, edit);
        }
    }

    delete form_parser;
    delete form_input;

    LineEdit* host_edit = this->args->value("host");
    if (host_edit == NULL) return;

    QMap<QString, QVariant> val = Monitor::getInstance()->targets->value(this->target).toMap();
    QString host = val.value("properties").toMap().value("host").toString();
    host_edit->setText(host);

}

bool NewProbePage2::validatePage() {

    QString probe_name(this->field("selection").toString());
    NewProbeProgressDialog* dial = new NewProbeProgressDialog(
            this->args,
            this->target,
            probe_name,
            this->probe_class,
            this->name_line->text(),
            this);
    int ret = dial->exec();
    if (ret == QMessageBox::Accepted) {
        return true;
    } else {
        return false;
    }

}

bool NewProbePage2::isComplete() const {

    for (int i = 0; i < this->mandatory_args->size(); ++i) {
        LineEdit *edit = this->mandatory_args->at(i);
        if (edit->text() == "") return false;
    }
    return true;

}

HelperExec::HelperExec(LineEdit* line, QWidget* parent) : QObject(parent) {

    this->h_class = "";
    this->h_target = "";
    this->w_parent = parent;
    this->flag_line = line;

}

void HelperExec::execHelper() {

    QMap<QString, QVariant> helperQuery;
    QMap<QString, QVariant> value;
    value.insert("target", this->h_target);
    value.insert("class", this->h_class);
    helperQuery.insert("from", "monitor");
    helperQuery.insert("type", "ncheckHelperQuery");
    helperQuery.insert("value", value);

    QString msg = QString("Executing helper %1").arg(this->h_class);
    this->dial = new QProgressDialog(this->w_parent);
    this->dial->setLabelText(msg);
    this->dial->setModal(true);
    this->dial->setMinimum(0);
    this->dial->setMaximum(0);
    this->dial->open();
    SupercastSignal* sig = new SupercastSignal();
    QObject::connect(
            sig, SIGNAL(serverMessage(QVariant)),
            this, SLOT(helperReply(QVariant)));
    Supercast::sendQuery(helperQuery, sig);

}

void HelperExec::helperReply(QVariant replyVariant) {

    QMap<QString, QVariant> reply = replyVariant.toMap();
    this->dial->close();
    this->dial->deleteLater();
    qDebug() << "helper success" << reply;

    QMap<QString, QVariant> reply_content = reply.value("value").toMap().value("reply").toMap();
    if (reply_content.value("status").toString() == "success") {
        if (reply_content.value("type").toString() == "simple") {
            QString value = reply_content.value("message").toString();
            this->flag_line->setText(value);
        } else if (reply_content.value("type").toString() == "table") {
            HelperDialog* hdial = new HelperDialog(reply_content, this->w_parent);
            if (hdial->exec() == QDialog::Accepted) {
                QString value = hdial->getValue();
                this->flag_line->setText(value);
            }
            hdial->deleteLater();
        }
    } else {
        MessageBox* mbox = new MessageBox(this->w_parent);
        mbox->setIconType(Sysmo::MESSAGE_ERROR);
        mbox->setModal(true);
        mbox->setWindowTitle(reply_content.value("id").toString());
        QString errMsg = reply_content.value("message").toString();
        if (errMsg.isEmpty()) {
            mbox->setText("The helper has fail with no error message");
        } else {
            mbox->setText(errMsg);
        }

        mbox->exec();
    }

}

HelperDialog::HelperDialog(
        QVariant helperReplyVariant,
        QWidget* parent) : QDialog(parent) {

    QMap<QString, QVariant> helperReply = helperReplyVariant.toMap();

    this->value = "";
    this->list_separator = "";
    this->setModal(true);
    this->setMinimumHeight(400);
    this->setMinimumWidth(600);
    this->setWindowTitle(helperReply.value("id").toString());

    NGrid* grid = new NGrid(this);
    this->setLayout(grid);

    QString label_text = helperReply.value("message").toString();
    QLabel* label = new QLabel(this);
    label->setText(label_text);
    grid->addWidget(label, 0, 0);

    QTreeWidget* tree = new QTreeWidget(this);
    tree->setSortingEnabled(true);
    tree->header()->setSortIndicatorShown(true);
    tree->setAlternatingRowColors(true);
    grid->addWidget(tree, 1, 0);

    QDialogButtonBox* button_box = new QDialogButtonBox(this);
    QPushButton* reset_button = button_box->addButton(QDialogButtonBox::Reset);
    QPushButton* save_button = button_box->addButton(QDialogButtonBox::Save);
    QPushButton* close_button = button_box->addButton(QDialogButtonBox::Close);

    QObject::connect(
            reset_button, SIGNAL(clicked(bool)),
            this, SLOT(resetTreeCheckState()));
    QObject::connect(
            save_button, SIGNAL(clicked(bool)),
            this, SLOT(validateSelection()));
    QObject::connect(
            close_button, SIGNAL(clicked(bool)),
            this, SLOT(reject()));

    grid->addWidget(button_box, 2, 0);
    grid->setRowStretch(0, 0);
    grid->setRowStretch(1, 1);
    grid->setRowStretch(2, 0);

    this->list_separator = helperReply.value("listSeparator").toString();
    QList<QVariant> all_rows = helperReply.value("rows").toList();

    if (helperReply.value("treeRoot").toString() != "") {
        /*
         * This is a table with tree
         */
        QString tree_root = helperReply.value("treeRoot").toString();


        /*
         * get all roots types
         */
        QStringList roots = QStringList();

        foreach(const QVariant row, all_rows) {
            QMap<QString, QVariant> row_obj = row.toMap();
            QString root = row_obj.value(tree_root).toString();
            if (roots.contains(root)) continue;
            roots.append(root);
        }
        qDebug() << "roots are: " << roots;

        /*
         * Create initial root items
         */
        foreach(const QString ritem, roots) {
            QString txt = QString("%1(%2)").arg(tree_root).arg(ritem);
            QStringList txt_list;
            txt_list.append(txt);
            QTreeWidgetItem* item = new QTreeWidgetItem(tree, txt_list, QTreeWidgetItem::Type);
            item->setCheckState(0, Qt::Unchecked);
            item->setFlags(item->flags() | Qt::ItemIsUserCheckable);
            this->root_items.insert(ritem, item);
            tree->addTopLevelItem(item);
        }


        /*
         * get all column types minus tree_root and set header
         */
        QMap<QString, QVariant> test_obj = all_rows.at(0).toMap();
        QStringList cols = test_obj.keys();
        cols.removeAll(tree_root);
        tree->setColumnCount(cols.size());
        tree->setHeaderLabels(cols);
        tree->setSelectionMode(QAbstractItemView::NoSelection);


        /*
         * Fill childs
         */
        QString select = helperReply.value("select").toString();

        foreach(const QVariant row, all_rows) {
            QMap<QString, QVariant> row_obj = row.toMap();
            QString iroot = row_obj.value(tree_root).toString();
            QTreeWidgetItem* root_item = this->root_items.value(iroot);
            QStringList item_cols;

            foreach(const QString key, cols) {
                item_cols.append(row_obj.value(key).toString());
            }

            QString item_data = row_obj.value(select).toString();
            QTreeWidgetItem* child_item = new QTreeWidgetItem(
                    item_cols, QTreeWidgetItem::Type);
            child_item->setData(0, Qt::UserRole, QVariant(item_data));
            child_item->setCheckState(0, Qt::Unchecked);
            child_item->setFlags(child_item->flags() | Qt::ItemIsUserCheckable);
            root_item->addChild(child_item);
        }



        /*
         * Selection propagation
         */
        QObject::connect(
                tree, SIGNAL(itemChanged(QTreeWidgetItem*, int)),
                this, SLOT(refreshTreeState(QTreeWidgetItem*, int)));

        tree->header()->resizeSections(QHeaderView::ResizeToContents);
        tree->expandAll();
    }

}

void HelperDialog::validateSelection() {

    QList<QTreeWidgetItem*> selection;
    QMap<QString, QTreeWidgetItem*>::iterator i;
    for (i = this->root_items.begin();
            i != this->root_items.end();
            i++) {
        QTreeWidgetItem* item = i.value();
        int child_count = item->childCount();
        for (int i = 0; i < child_count; i++) {
            QTreeWidgetItem* child = item->child(i);
            if (child->checkState(0) == Qt::Checked) {
                selection.append(child);
            }
        }
    }

    for (int j = 0; j < selection.count(); j++) {
        if (j != 0) this->value.append(this->list_separator);
        this->value.append(selection[j]->data(0, Qt::UserRole).toString());
    }
    emit this->accept();

}

void HelperDialog::resetTreeCheckState() {

    QMap<QString, QTreeWidgetItem*>::iterator i;
    for (i = this->root_items.begin();
            i != this->root_items.end();
            i++) {
        QTreeWidgetItem* item = i.value();
        int child_count = item->childCount();
        for (int i = 0; i < child_count; i++) {
            QTreeWidgetItem* child = item->child(i);
            if (child->checkState(0) != Qt::Unchecked) {
                child->setCheckState(0, Qt::Unchecked);
            }
        }

    }

}

void HelperDialog::refreshTreeState(QTreeWidgetItem *item, int column) {

    Q_UNUSED(column);
    int child_count = item->childCount();
    if (child_count > 0) { // it is a root item
        if (item->checkState(0) == Qt::PartiallyChecked) return;
        Qt::CheckState root_state = item->checkState(0);
        for (int i = 0; i < child_count; i++) {
            QTreeWidgetItem* child = item->child(i);
            if (child->checkState(0) != root_state) {
                child->setCheckState(0, root_state);
            }
        }
    } else { // it is a child item may influence root item
        QTreeWidgetItem* root_item = item->parent();
        // get the number of child of the parent
        int root_count = root_item->childCount();
        // generate a state list
        QList<Qt::CheckState> states_list;
        for (int i = 0; i < root_count; i++) {
            QTreeWidgetItem* child_item = root_item->child(i);
            states_list.append(child_item->checkState(0));
        }

        // if checked and unchecked are present root is tristate
        if (states_list.contains(Qt::Unchecked) &&
                states_list.contains(Qt::Checked)) {
            if (root_item->checkState(0) != Qt::PartiallyChecked)
                root_item->setCheckState(0, Qt::PartiallyChecked);
        } else if (states_list.contains(Qt::Checked)) { // all is checked
            if (root_item->checkState(0) != Qt::Checked)
                root_item->setCheckState(0, Qt::Checked);
        } else { // all is unchecked
            if (root_item->checkState(0) != Qt::Unchecked)
                root_item->setCheckState(0, Qt::Unchecked);
        }
    }

    // set apply button state
}

QString HelperDialog::getValue() {

    /*
     * TODO return selected items
     */
    return this->value;

}
