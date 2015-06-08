#ifndef SYSMO
#define SYSMO

#include <Qt>

namespace Sysmo {

    // QStandardItem::type()
    const int TYPE_TARGET         = 1000;
    const int TYPE_PROBE          = 1001;

    // QStandardItem::data(role);
    const int ROLE_PROBE_STATUS     = Qt::UserRole + 1;
    const int ROLE_IS_PROGRESS_ITEM = Qt::UserRole + 2;
    const int ROLE_PROGRESS_STEP    = Qt::UserRole + 3;
    const int ROLE_PROGRESS_NEXT    = Qt::UserRole + 4;

    // Probe return status
    const int STATUS_OK       = 0;
    const int STATUS_UNKNOWN  = 10;
    const int STATUS_ERROR    = 20;
    const int STATUS_WARNING  = 30;
    const int STATUS_CRITICAL = 40;
}

#endif // SYSMO
