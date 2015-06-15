#ifndef SYSMO
#define SYSMO

#include <Qt>

namespace Sysmo {

    // Message box status
    const int MESSAGE_INFO     = 0;
    const int MESSAGE_WARNING  = 1;
    const int MESSAGE_ERROR    = 2;

    // QStandardItem::type() and data(Sysmo::ROLE_TYPE)
    const int TYPE_TARGET         = 1000;
    const int TYPE_PROBE          = 1001;

    // QStandardItem::data(role);
    const int ROLE_PROBE_STATUS     = Qt::UserRole + 1;
    const int ROLE_IS_PROGRESS_ITEM = Qt::UserRole + 2;
    const int ROLE_PROGRESS_STEP    = Qt::UserRole + 3;
    const int ROLE_PROGRESS_NEXT    = Qt::UserRole + 4;
    const int ROLE_FILTER_STRING    = Qt::UserRole + 5;
    const int ROLE_ELEMENT_NAME     = Qt::UserRole + 6;
    const int ROLE_TYPE             = Qt::UserRole + 7;

    // Probe return status
    const int STATUS_OK       = 0;
    const int STATUS_UNKNOWN  = 10;
    const int STATUS_ERROR    = 20;
    const int STATUS_WARNING  = 30;
    const int STATUS_CRITICAL = 40;

    // SNMP versions
    const int SNMP_VERSION_3                = 0;
    const int SNMP_VERSION_2                = 1;
    const int SNMP_VERSION_1                = 2;
    // SNMP auth protocol
    const int SNMP_AUTH_SHA                 = 0;
    const int SNMP_AUTH_MD5                 = 1;
    // SNMP priv protocol
    const int SNMP_PRIV_AES128              = 0;
    const int SNMP_PRIV_DES                 = 10;
    const int SNMP_PRIV_AES192              = 20;
    const int SNMP_PRIV_AES256              = 30;
    const int SNMP_PRIV_3DES                = 40;
    // SNMP seclevel
    const int SNMP_SECLEVEL_AUTH_PRIV       = 0;
    const int SNMP_SECLEVEL_AUTH_NO_PRIV    = 1;
    const int SNMP_SECLEVEL_NO_AUTH_NO_PRIV = 2;
}

#endif // SYSMO
