#
# Sysmo-Operator build
#
project(Sysmo-Operator)
enable_language(CXX)


#
# cmake_minimum_required(VERSION 2.8.11)
# 2.8.11 required for Qt5 build but travis uses 2.8.7 on osx
#
cmake_minimum_required(VERSION 2.8)
if (CMAKE_VERSION VERSION_LESS 2.8.11)
    # WARNING
else()
    cmake_policy(SET CMP0020 NEW)
endif (CMAKE_VERSION VERSION_LESS 2.8.11)


#
# For more interesing log messages (qDebug)
#
add_definitions(-DQT_MESSAGELOGCONTEXT)


set (OPERATOR_VERSION_MAJOR "2")
set (OPERATOR_VERSION_MINOR "0")
set (OPERATOR_VERSION_PATCH "10")
set (OPERATOR_VERSION "${OPERATOR_VERSION_MAJOR}.${OPERATOR_VERSION_MINOR}.${OPERATOR_VERSION_PATCH}")


#
# Get rrdio libraries names and versions for rrdio.qrc.in and config.h.in
#
add_subdirectory(ressources/)


#
# Configure files
#
message("-- Configure code/config.h")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/code/config.h.in
    ${CMAKE_CURRENT_SOURCE_DIR}/code/config.h)
message("-- Configure support/packages/obs/_service")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/support/packages/obs/_service.in
    ${CMAKE_CURRENT_SOURCE_DIR}/support/packages/obs/_service)
message("-- Configure ressources/rrdio.qrc")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/ressources/rrdio.qrc.in
    ${CMAKE_CURRENT_SOURCE_DIR}/ressources/rrdio.qrc)


#
# Operator SRC in one CMakeLists.txt file is simpler. CMake automaticaly
# handle headers dependencies.
#
set (OPERATOR_SRC
    code/main.cpp
    code/sysmo.h
    code/config.h
    code/mainwindow.cpp
    code/login.cpp
    code/login.h
    code/centralwidget.cpp
    code/centralwidget.h
    code/themes.cpp
    code/themes.h
    code/logs/clog.h
    code/logs/clog.c
    code/widgets/lineedit.cpp
    code/widgets/lineedit.h
    code/widgets/messagebox.cpp
    code/widgets/messagebox.h
    code/widgets/nframecontainer.cpp
    code/widgets/nframecontainer.h
    code/widgets/nframe.cpp
    code/widgets/nframe.h
    code/widgets/ngridcontainer.cpp
    code/widgets/ngridcontainer.h
    code/widgets/ngrid.cpp
    code/widgets/ngrid.h
    code/widgets/nowheelcombobox.cpp
    code/widgets/nowheelcombobox.h
    code/widgets/sidebutton.cpp
    code/widgets/sidebutton.h
    code/widgets/statusbutton.cpp
    code/widgets/statusbutton.h
    code/widgets/statusbuttonwidget.cpp
    code/widgets/statusbuttonwidget.h
    code/widgets/systemtray.cpp
    code/widgets/systemtray.h
    code/widgets/temporarydir.cpp
    code/widgets/temporarydir.h
    code/applications/dashboard/dashboardtab.cpp
    code/applications/dashboard/dashboardtab.h
    code/applications/dashboard/dashboardwidget.cpp
    code/applications/dashboard/dashboardwidget.h
    code/applications/dashboard/dialogs/newdashboard.cpp
    code/applications/dashboard/dialogs/newdashboard.h
    code/applications/dashboard/dialogs/newdashboardp1.cpp
    code/applications/dashboard/dialogs/newdashboardp1.h
    code/applications/logs/logswidget.cpp
    code/applications/logs/logswidget.h
    code/applications/monitor/dialogs/newprobe.cpp
    code/applications/monitor/dialogs/newprobe.h
    code/applications/monitor/dialogs/newprobepage1.cpp
    code/applications/monitor/dialogs/newprobepage1.h
    code/applications/monitor/dialogs/newprobepage2.cpp
    code/applications/monitor/dialogs/newprobepage2.h
    code/applications/monitor/dialogs/newprobepage3.cpp
    code/applications/monitor/dialogs/newprobepage3.h
    code/applications/monitor/dialogs/newprobeprogressdialog.cpp
    code/applications/monitor/dialogs/newprobeprogressdialog.h
    code/applications/monitor/dialogs/newtarget.cpp
    code/applications/monitor/dialogs/newtarget.h
    code/applications/monitor/dialogs/newtargetpage1.cpp
    code/applications/monitor/dialogs/newtargetpage1.h
    code/applications/monitor/actions/actionprocess.cpp
    code/applications/monitor/actions/actionprocess.h
    code/applications/monitor/actions/monitoractionconfig.cpp
    code/applications/monitor/actions/monitoractionconfig.h
    code/applications/monitor/actions/monitoractioncreate.cpp
    code/applications/monitor/actions/monitoractioncreate.h
    code/applications/monitor/actions/monitoractions.cpp
    code/applications/monitor/actions/monitoractionsdialog.cpp
    code/applications/monitor/actions/monitoractionsdialog.h
    code/applications/monitor/actions/monitoractions.h
    code/applications/monitor/targetutils.h
    code/applications/monitor/delegateprobeprogress.cpp
    code/applications/monitor/delegateprobeprogress.h
    code/applications/monitor/itemprobe.cpp
    code/applications/monitor/itemprobe.h
    code/applications/monitor/itemtarget.cpp
    code/applications/monitor/itemtarget.h
    code/applications/monitor/menuprobe.cpp
    code/applications/monitor/menuprobe.h
    code/applications/monitor/menutarget.cpp
    code/applications/monitor/menutarget.h
    code/applications/monitor/monitorchannel.cpp
    code/applications/monitor/monitorchannel.h
    code/applications/monitor/monitor.cpp
    code/applications/monitor/monitor.h
    code/applications/monitor/monitorlogs.cpp
    code/applications/monitor/monitorlogs.h
    code/applications/monitor/monitorwidget.cpp
    code/applications/monitor/monitorwidget.h
    code/applications/monitor/nchecks.cpp
    code/applications/monitor/nchecks.h
    code/applications/monitor/treemodel.cpp
    code/applications/monitor/treemodel.h
    code/applications/monitor/treeview.cpp
    code/applications/monitor/treeview.h
    code/applications/monitor/xml/parseallchecks.cpp
    code/applications/monitor/xml/parseallchecks.h
    code/applications/monitor/xml/parsecheckgetid.cpp
    code/applications/monitor/xml/parsecheckgetid.h
    code/applications/monitor/xml/parsecheckgetinfos.cpp
    code/applications/monitor/xml/parsecheckgetinfos.h
    code/applications/monitor/xml/parsecheckmakedoc.cpp
    code/applications/monitor/xml/parsecheckmakedoc.h
    code/applications/monitor/xml/parsecheckmakeform.cpp
    code/applications/monitor/xml/parsecheckmakeform.h
    code/applications/monitor/xml/parsecheckmakegraphcmd.cpp
    code/applications/monitor/xml/parsecheckmakegraphcmd.h
    code/applications/monitor/windows/probewindow.cpp
    code/applications/monitor/windows/probewindow.h
    code/network/supercast.cpp
    code/network/supercast.h
    code/network/supercasthttp.cpp
    code/network/supercasthttp.h
    code/network/supercasthttpreply.cpp
    code/network/supercasthttpreply.h
    code/network/supercasthttprequest.cpp
    code/network/supercasthttprequest.h
    code/network/supercastsignal.cpp
    code/network/supercastsignal.h
    code/network/qjson.h
    code/network/qjson.cpp
    code/network/socketutils.h
    code/network/socketutils.cpp
    code/rrds/rrd4qt.cpp
    code/rrds/rrd4qtgraph.cpp
    code/rrds/rrd4qtgraph.h
    code/rrds/rrd4qt.h
    code/rrds/rrd4qtproc.cpp
    code/rrds/rrd4qtproc.h
    code/rrds/rrd4qtsignal.cpp
    code/rrds/rrd4qtsignal.h)


#
# Every sysmo-operator Qt ressources
#
set (OPERATOR_QRC
    ressources/icons.qrc
    ressources/box_icons.qrc
    ressources/images.qrc
    ressources/pixmaps.qrc
    ressources/tree.qrc
    ressources/rrdio.qrc
    ressources/cssressource.qrc
    ressources/darcula.qrc
    ressources/operator-ui.qrc)



#
# Find Qt (4 or 5), and set correct libs/includes/ressources
#
set (OPERATOR_LIBS "")
set (OPERATOR_QRCS "")
set (OPERATOR_INCLUDES "")
find_package(Qt4 QUIET)
if (QT4_FOUND)
    message(STATUS "QtWebsockets not supported. Fallback to TCP.")
    find_package (Qt4 REQUIRED QtCore QtGui QtNetwork QtXml)
    include (${QT_USE_FILE})
    set (OPERATOR_INCLUDES
        ${Qt4Core_INCLUDE_DIRS}
        ${Qt4Gui_INCLUDE_DIRS}
        ${Qt4Network_INCLUDE_DIRS}
        ${Qt4Xml_INCLUDE_DIRS})
    set (OPERATOR_SRC ${OPERATOR_SRC}
        code/network/supercastsocket.cpp
        code/network/supercastsocket.h)
    set (OPERATOR_LIBS ${QT_LIBRARIES})
    QT4_ADD_RESOURCES(OPERATOR_QRCS ${OPERATOR_QRC})
else()
    find_package(Qt5Widgets REQUIRED)
    find_package(Qt5Core REQUIRED)
    find_package(Qt5Gui REQUIRED)
    find_package(Qt5Xml REQUIRED)
    find_package(Qt5Network REQUIRED)
    set (OPERATOR_INCLUDES
        ${Qt5Widgets_INCLUDE_DIRS}
        ${Qt5Core_INCLUDE_DIRS}
        ${Qt5Gui_INCLUDE_DIRS}
        ${Qt5Network_INCLUDE_DIRS}
        ${Qt5Xml_INCLUDE_DIRS})
    set (OPERATOR_LIBS
        Qt5::Core
        Qt5::Gui
        Qt5::Network
        Qt5::Xml
        Qt5::Widgets)
    # Use websocket if available
    find_package(Qt5WebSockets QUIET)
    if (Qt5WebSockets_FOUND)
        message(STATUS "QtWebsockets found.")
        add_definitions(-DUSE_WEBSOCKET)
        find_package(Qt5Websockets REQUIRED)
        set (OPERATOR_INCLUDES
            ${OPERATOR_INCLUDES}
            ${Qt5WebSockets_INCLUDE_DIRS})
        set(OPERATOR_LIBS
            ${OPERATOR_LIBS}
            Qt5::WebSockets)
        set (OPERATOR_SRC
            ${OPERATOR_SRC}
            code/network/supercastwebsocket.cpp
            code/network/supercastwebsocket.h)
    else()
        message(STATUS "QtWebsockets not supported. Fallback to TCP.")
        set (OPERATOR_SRC
            ${OPERATOR_SRC}
            code/network/supercastsocket.cpp
            code/network/supercastsocket.h)
    endif (Qt5WebSockets_FOUND)
    QT5_ADD_RESOURCES(OPERATOR_QRCS ${OPERATOR_QRC})
endif(QT4_FOUND)


#
# This is allmost it!
#
set (CMAKE_AUTORCC ON)
set (CMAKE_AUTOMOC ON)
include_directories(code ${OPERATOR_INCLUDES})
add_executable(sysmo-operator ${OPERATOR_SRC} ${OPERATOR_QRCS})


#
# If WIN32, we must set an executable icon (MSVC ressource system),
# and link with SUBSYSTEM:WINDOWS to avoid CMD window.
#
if (WIN32)
    if(MSVC)

        # Suppress incorrect warnings
        add_definitions("/D _CRT_SECURE_NO_WARNINGS")

        # Needed for windowed applications
        set_target_properties(sysmo-operator PROPERTIES
            LINK_FLAGS "/SUBSYSTEM:WINDOWS")
        set(OPERATOR_LIBS ${OPERATOR_LIBS} Qt5::WinMain)

        # Icon for executable
        message("-- Configure support/packages/win/icon-ressource.rc")
        configure_file(
            ${CMAKE_CURRENT_SOURCE_DIR}/support/packages/win/icon-ressource.rc.in
            ${CMAKE_BINARY_DIR}/icon-ressource.rc)
        add_custom_command(
            TARGET sysmo-operator PRE_BUILD
            COMMAND rc /fo ${CMAKE_BINARY_DIR}/icon-ressource.res ${CMAKE_BINARY_DIR}/icon-ressource.rc)
        set(OPERATOR_LIBS
            ${OPERATOR_LIBS}
            ${CMAKE_BINARY_DIR}/icon-ressource.res)

    endif(MSVC)
endif(WIN32)


#
# The END
#
target_link_libraries(sysmo-operator ${OPERATOR_LIBS})


#
# WIN32 Dependency scan section, we use QT5_WINDEPOYQT:
#
if (WIN32)
    set(WIX_SOURCE_DIR $<TARGET_FILE_DIR:sysmo-operator>)
    get_target_property(QT5_QMAKE_EXECUTABLE Qt5::qmake IMPORTED_LOCATION)
    get_filename_component(QT5_WINDEPLOYQT_EXECUTABLE
        ${QT5_QMAKE_EXECUTABLE} PATH)
    set(QT5_WINDEPLOYQT_EXECUTABLE
        "${QT5_WINDEPLOYQT_EXECUTABLE}/windeployqt.exe")
    add_custom_command(TARGET sysmo-operator POST_BUILD
        COMMAND ${QT5_WINDEPLOYQT_EXECUTABLE} --qmldir ${CMAKE_SOURCE_DIR} $<TARGET_FILE_DIR:sysmo-operator>)

    install (DIRECTORY $<TARGET_FILE_DIR:sysmo-operator>/ DESTINATION .)
endif(WIN32)


#
# Windows package with CPack.
#
# The bundle is generated from support/packages/generate_bundle.cmd.
#
if (WIN32)
    set (CPACK_PACKAGE_NAME "Sysmo-Operator")
    set (CPACK_PACKAGE_VENDOR "Sysmo NMS")
    set (CPACK_PACKAGE_CONTACT "contact@sysmo.io")
    set (CPACK_PACKAGE_DESCRIPTION_SUMMARY "Sysmo-NMS user interface")
    set (CPACK_PACKAGE_INSTALL_DIRECTORY "Sysmo NMS/Sysmo-Operator")
    set (CPACK_PACKAGE_INSTALL_REGISTRY_KEY "sysmo-operator/${OPERATOR_VERSION}")
    set (CPACK_PACKAGE_VERSION_MAJOR ${OPERATOR_VERSION_MAJOR})
    set (CPACK_PACKAGE_VERSION_MINOR ${OPERATOR_VERSION_MINOR})
    set (CPACK_PACKAGE_VERSION_PATCH ${OPERATOR_VERSION_PATCH})
    if (NOT DEFINED ENV{PLATFORM})
        set (BUILD_PLATFORM ${CPACK_SYSTEM_NAME})
    else()
        set (BUILD_PLATFORM $ENV{PLATFORM})
    endif(NOT DEFINED ENV{PLATFORM})

    if ("${BUILD_PLATFORM}" STREQUAL "")
        set (BUILD_PLATFORM ${CPACK_SYSTEM_NAME})
    endif()

    if ("${BUILD_PLATFORM}" STREQUAL "Win32")
        set (BUILD_PLATFORM "i586")
    endif()

    set (CPACK_PACKAGE_FILE_NAME "__installer-${BUILD_PLATFORM}")
    set (CPACK_STRIP_FILES 1)
    set (CPACK_SOURCE_STRIP_FILES 1)
    set (CPACK_CREATE_DESKTOP_LINKS 1)
    set (CPACK_INCLUDE_TOP_LEVEL_DIRECTORY 1)
    set (CPACK_INSTALLED_DIRECTORIES $<TARGET_FILE_DIR:sysmo-operator>/ .)
    set (CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE.txt")
    set (CPACK_PACKAGE_EXECUTABLES sysmo-operator "Sysmo-Operator")

    set (CPACK_GENERATOR WIX)
    set (CPACK_WIX_UPGRADE_GUID "8999771C-F49B-462C-AB3D-CD84432DD585")
    set (CPACK_WIX_PRODUCT_ICON "${CMAKE_CURRENT_SOURCE_DIR}/support/packages/win/logo.png")

    message("-- Configure support/package/win/bundle.wxs")
    configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/support/packages/win/bundle.wxs.in
        ${CMAKE_BINARY_DIR}/bundle.wxs)

    message("-- Configure support/package/win/bin/generate_bundle.cmd")
    configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/support/packages/win/bin/generate_bundle.cmd.in
        ${CMAKE_BINARY_DIR}/generate_bundle.cmd)


    include(CPack)
endif(WIN32)


