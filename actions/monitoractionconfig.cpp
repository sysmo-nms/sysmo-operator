#include "monitoractionconfig.h"

MonitorActionConfig::MonitorActionConfig(QWidget* parent, QString target)
        : QDialog(parent)
{

    this->target = target;
    this->setMinimumHeight(200);
    this->setMinimumWidth(500);


    QLabel *label = new QLabel(this);
    label->setText("Configure actions tool");
    this->tree_widget = new QTreeWidget(this);
    QStringList header;
    header << "Name" << "Executable" << "Default";
    this->tree_widget->setHeaderLabels(header);

    QDialogButtonBox *buttonBox = new QDialogButtonBox(this);
    buttonBox->addButton(QDialogButtonBox::Close);
    QPushButton *close = buttonBox->button(QDialogButtonBox::Close);
    QObject::connect(
                close, SIGNAL(clicked(bool)),
                this,  SLOT(close()));

    NFrame *frame = new NFrame(this);

    NGrid *grid = new NGrid();
    frame->setLayout(grid);
    grid->addWidget(label, 0,0);
    grid->addWidget(this->tree_widget, 1,0);
    grid->addWidget(buttonBox, 2,0);


    NGridContainer *gcontainer = new NGridContainer(this);
    gcontainer->addWidget(frame);
}

