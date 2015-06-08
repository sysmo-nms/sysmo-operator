#ifndef SYSMO
#define SYSMO

#include <Qt>

namespace Sysmo {
    const int TYPE_TARGET           = 1000;
    const int TYPE_TARGET_TYPE      = 1001;
    const int TYPE_PROBE            = 1002;
    const int TYPE_PROBE_PROGRESS   = 1003;
    const int ROLE_PROBE_STATUS     = Qt::UserRole + 1;
    const int ROLE_IS_PROGRESS_ITEM = Qt::UserRole + 2;
}

#endif // SYSMO

