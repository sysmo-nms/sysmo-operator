#ifndef SYSMO
#define SYSMO

#include <Qt>

namespace Sysmo {

    /*
     * Message box status
     */
    const int MESSAGE_INFO     = 0;
    const int MESSAGE_WARNING  = 1;
    const int MESSAGE_ERROR    = 2;


    /*
     * QStandardItem::type() and data(Sysmo::ROLE_TYPE)
     */
    const int TYPE_TARGET = 1000;
    const int TYPE_PROBE  = 1001;


    /*
     * QStandardItem::data(role);
     */
    const int ROLE_PROBE_STATUS     = Qt::UserRole + 1;
    const int ROLE_IS_PROGRESS_ITEM = Qt::UserRole + 2;
    const int ROLE_PROGRESS_STEP    = Qt::UserRole + 3;
    const int ROLE_PROGRESS_NEXT    = Qt::UserRole + 4;
    const int ROLE_FILTER_STRING    = Qt::UserRole + 5;
    const int ROLE_ELEMENT_NAME     = Qt::UserRole + 6;
    const int ROLE_TYPE             = Qt::UserRole + 7;
    const int ROLE_FILTER_ORIG      = Qt::UserRole + 8;


    /*
     * Probe return status
     */
    const int STATUS_OK       = 0;
    const int STATUS_UNKNOWN  = 1;
    const int STATUS_ERROR    = 2;
    const int STATUS_WARNING  = 3;
    const int STATUS_CRITICAL = 4;


    /*
     * SNMP
     */

    // versions
    const int SNMP_VERSION_3 = 0;
    const int SNMP_VERSION_2 = 1;
    const int SNMP_VERSION_1 = 2;

    // auth protocol
    const int SNMP_AUTH_SHA = 0;
    const int SNMP_AUTH_MD5 = 1;

    // priv protocol
    const int SNMP_PRIV_AES128 = 0;
    const int SNMP_PRIV_DES    = 1;
    const int SNMP_PRIV_AES192 = 2;
    const int SNMP_PRIV_AES256 = 3;
    const int SNMP_PRIV_3DES   = 4;

    // seclevel
    const int SNMP_SECLEVEL_AUTH_PRIV       = 0;
    const int SNMP_SECLEVEL_AUTH_NO_PRIV    = 1;
    const int SNMP_SECLEVEL_NO_AUTH_NO_PRIV = 2;


    /*
     * Restart application code
     */
    const int APP_RESTART_CODE = 1000;

    /*
     * Socket timeout
     */
    const int SUPERCAST_SOCKET_TIMEOUT = 4000;
}

#endif // SYSMO
