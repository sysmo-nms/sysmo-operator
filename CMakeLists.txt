# cmake_minimum_required(VERSION 2.8.11)
# 2.8.11 required for Qt5 build but travis uses 2.8.7 on osx
cmake_minimum_required(VERSION 2.8)
if (CMAKE_VERSION VERSION_LESS 2.8.11)
    # WARNING
else()
    cmake_policy(SET CMP0020 NEW)
endif (CMAKE_VERSION VERSION_LESS 2.8.11)


project(Sysmo-Operator)
set (OPERATOR_VERSION_MAJOR "2")
set (OPERATOR_VERSION_MINOR "0")
set (OPERATOR_VERSION_PATCH "2")
set (OPERATOR_VERSION "${OPERATOR_VERSION_MAJOR}.${OPERATOR_VERSION_MINOR}.${OPERATOR_VERSION_PATCH}")
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/code/operator_version.h.in
    ${CMAKE_CURRENT_SOURCE_DIR}/code/operator_version.h)


set (OPERATOR_SRC
    code/main.cpp
    code/updates/updates.cpp
    code/updates/updates.h
    code/actions/actionprocess.cpp
    code/actions/actionprocess.h
    code/actions/monitoractionconfig.cpp
    code/actions/monitoractionconfig.h
    code/actions/monitoractioncreate.cpp
    code/actions/monitoractioncreate.h
    code/actions/monitoractions.cpp
    code/actions/monitoractionsdialog.cpp
    code/actions/monitoractionsdialog.h
    code/actions/monitoractions.h
    code/centralwidget.cpp
    code/centralwidget.h
    code/dashboard/dashboardtab.cpp
    code/dashboard/dashboardtab.h
    code/dashboard/dashboardwidget.cpp
    code/dashboard/dashboardwidget.h
    code/dialogs/login.cpp
    code/dialogs/login.h
    code/dialogs/messagebox.cpp
    code/dialogs/messagebox.h
    code/dialogs/newprobe.cpp
    code/dialogs/newprobe.h
    code/dialogs/newprobepage1.cpp
    code/dialogs/newprobepage1.h
    code/dialogs/newprobepage2.cpp
    code/dialogs/newprobepage2.h
    code/dialogs/newprobepage3.cpp
    code/dialogs/newprobepage3.h
    code/dialogs/newprobeprogressdialog.cpp
    code/dialogs/newprobeprogressdialog.h
    code/dialogs/newtarget.cpp
    code/dialogs/newtarget.h
    code/dialogs/newtargetpage1.cpp
    code/dialogs/newtargetpage1.h
    code/lineedit.cpp
    code/lineedit.h
    code/mainwindow.cpp
    code/monitor/delegateprobeprogress.cpp
    code/monitor/delegateprobeprogress.h
    code/monitor/itemprobe.cpp
    code/monitor/itemprobe.h
    code/monitor/itemtarget.cpp
    code/monitor/itemtarget.h
    code/monitor/menuprobe.cpp
    code/monitor/menuprobe.h
    code/monitor/menutarget.cpp
    code/monitor/menutarget.h
    code/monitor/monitorchannel.cpp
    code/monitor/monitorchannel.h
    code/monitor/monitor.cpp
    code/monitor/monitor.h
    code/monitor/monitorlogs.cpp
    code/monitor/monitorlogs.h
    code/monitor/monitorwidget.cpp
    code/monitor/monitorwidget.h
    code/monitor/nchecks.cpp
    code/monitor/nchecks.h
    code/monitor/treemodel.cpp
    code/monitor/treemodel.h
    code/monitor/treeview.cpp
    code/monitor/treeview.h
    code/monitor/xml/parseallchecks.cpp
    code/monitor/xml/parseallchecks.h
    code/monitor/xml/parsecheckgetid.cpp
    code/monitor/xml/parsecheckgetid.h
    code/monitor/xml/parsecheckgetinfos.cpp
    code/monitor/xml/parsecheckgetinfos.h
    code/monitor/xml/parsecheckmakedoc.cpp
    code/monitor/xml/parsecheckmakedoc.h
    code/monitor/xml/parsecheckmakeform.cpp
    code/monitor/xml/parsecheckmakeform.h
    code/monitor/xml/parsecheckmakegraphcmd.cpp
    code/monitor/xml/parsecheckmakegraphcmd.h
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
    code/nframecontainer.cpp
    code/nframecontainer.h
    code/nframe.cpp
    code/nframe.h
    code/ngridcontainer.cpp
    code/ngridcontainer.h
    code/ngrid.cpp
    code/ngrid.h
    code/nowheelcombobox.cpp
    code/nowheelcombobox.h
    code/rrds/rrd4qt.cpp
    code/rrds/rrd4qtgraph.cpp
    code/rrds/rrd4qtgraph.h
    code/rrds/rrd4qt.h
    code/rrds/rrd4qt_config.h
    code/rrds/rrd4qtproc.cpp
    code/rrds/rrd4qtproc.h
    code/rrds/rrd4qtsignal.cpp
    code/rrds/rrd4qtsignal.h
    code/sidebutton.cpp
    code/sidebutton.h
    code/statusbutton.cpp
    code/statusbutton.h
    code/statusbuttonwidget.cpp
    code/statusbuttonwidget.h
    code/sysmo.h
    code/systemtray.cpp
    code/systemtray.h
    code/temporarydir.cpp
    code/temporarydir.h
    code/themes.cpp
    code/themes.h
    code/windows/probewindow.cpp
    code/windows/probewindow.h
    code/qjson.h
    code/qjson.cpp)

set (OPERATOR_QRC
    support/icons.qrc
    support/box_icons.qrc
    support/images.qrc
    support/pixmaps.qrc
    support/tree.qrc
    support/rrdio.qrc
    support/cssressource.qrc)

add_definitions(-DQT_MESSAGELOGCONTEXT)


# dependencies
set (OPERATOR_DEPS_INCLUDES  "")
set (OPERATOR_DEPS_LIBRARIES "")

# add deps will build rrdio
add_subdirectory(deps/)
# add support will build rrdio.qrc
add_subdirectory(support/)
# configure rrd4qt
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/code/rrds/rrd4qt_config.h.in
    ${CMAKE_CURRENT_SOURCE_DIR}/code/rrds/rrd4qt_config.h)

# qt
set (OPERATOR_QT_LIBRARIES "")
set (OPERATOR_QT_INCLUDES "")
set (OPERATOR_QT_RESSOURCES "")
find_package(Qt4 QUIET)
if (QT4_FOUND)

    message(STATUS "QtWebsockets not supported. Fallback to TCP.")
    find_package (Qt4 REQUIRED QtCore QtGui QtNetwork QtXml)
    include (${QT_USE_FILE})
    set (OPERATOR_QT_INCLUDES
        ${Qt4Core_INCLUDE_DIRS}
        ${Qt4Gui_INCLUDE_DIRS}
        ${Qt4Network_INCLUDE_DIRS}
        ${Qt4Xml_INCLUDE_DIRS})

    set (OPERATOR_SRC ${OPERATOR_SRC}
        code/network/supercastsocket.cpp
        code/network/supercastsocket.h)

    set (OPERATOR_QT_LIBRARIES ${QT_LIBRARIES})
    QT4_ADD_RESOURCES(OPERATOR_QT_RESSOURCES ${OPERATOR_QRC})

else()

    find_package(Qt5Widgets REQUIRED)
    find_package(Qt5Core REQUIRED)
    find_package(Qt5Gui REQUIRED)
    find_package(Qt5Xml REQUIRED)
    find_package(Qt5Network REQUIRED)
    set (OPERATOR_QT_INCLUDES
        ${Qt5Widgets_INCLUDE_DIRS}
        ${Qt5Core_INCLUDE_DIRS}
        ${Qt5Gui_INCLUDE_DIRS}
        ${Qt5Network_INCLUDE_DIRS}
        ${Qt5Xml_INCLUDE_DIRS})
    set (OPERATOR_QT_LIBRARIES
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
        set (OPERATOR_QT_INCLUDES
            ${OPERATOR_QT_INCLUDES}
            ${Qt5WebSockets_INCLUDE_DIRS})
        set(OPERATOR_QT_LIBRARIES
            ${OPERATOR_QT_LIBRARIES}
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

    QT5_ADD_RESOURCES(OPERATOR_QT_RESSOURCES ${OPERATOR_QRC})


endif(QT4_FOUND)


# finally
set (CMAKE_AUTORCC ON)
set (CMAKE_AUTOMOC ON)

add_executable(sysmo-operator
    ${OPERATOR_SRC}
    ${OPERATOR_QT_RESSOURCES})

if (WIN32)
    if(MSVC)

        # Suppress incorrect warnings
        add_definitions("/D _CRT_SECURE_NO_WARNINGS")

        # Needed for windowed applications
        set_target_properties(sysmo-operator PROPERTIES
            LINK_FLAGS "/SUBSYSTEM:WINDOWS")
        set(OPERATOR_QT_LIBRARIES ${OPERATOR_QT_LIBRARIES} Qt5::WinMain)

        # Icon for executable
        configure_file(
            ${CMAKE_CURRENT_SOURCE_DIR}/support/pkgs/win/icon-ressource.rc.in
            ${CMAKE_BINARY_DIR}/icon-ressource.rc)
        add_custom_command(
            TARGET sysmo-operator PRE_BUILD
            COMMAND rc /fo ${CMAKE_BINARY_DIR}/icon-ressource.res ${CMAKE_BINARY_DIR}/icon-ressource.rc)
        set(OPERATOR_DEPS_LIBRARIES
            ${OPERATOR_DEPS_LIBRARIES}
            ${CMAKE_BINARY_DIR}/icon-ressource.res)

    endif(MSVC)
endif(WIN32)

include_directories (
    code/
    deps/md5/
    ${OPERATOR_QT_INCLUDES}
    ${OPERATOR_DEPS_INCLUDES})

target_link_libraries(sysmo-operator
    ${OPERATOR_QT_LIBRARIES}
    ${OPERATOR_DEPS_LIBRARIES} md5)

# WIN32 Install...
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

# Windows package
if (WIN32)
    set (CPACK_PACKAGE_NAME "Sysmo-Operator")
    set (CPACK_PACKAGE_VENDOR "Sysmo NMS")
    set (CPACK_PACKAGE_CONTACT "contact@sysmo.io")
    set (CPACK_PACKAGE_DESCRIPTION_SUMMARY "Sysmo-NMS user interface")
    set (CPACK_PACKAGE_INSTALL_DIRECTORY "Sysmo NMS/Operator")
    set (CPACK_PACKAGE_INSTALL_REGISTRY_KEY "sysmo-operator/${OPERATOR_VERSION}")
    set (CPACK_PACKAGE_VERSION_MAJOR ${OPERATOR_VERSION_MAJOR})
    set (CPACK_PACKAGE_VERSION_MINOR ${OPERATOR_VERSION_MINOR})
    set (CPACK_PACKAGE_VERSION_PATCH ${OPERATOR_VERSION_PATCH})
    if (NOT DEFINED ENV{PLATFORM})
       set (BUILD_PLATFORM ${CPACK_SYSTEM_NAME})
    else()
        if ($ENV{PLATFORM} STREQUAL "")
            set (BUILD_PLATFORM ${CPACK_SYSTEM_NAME})
        else()
            set (BUILD_PLATFORM $ENV{PLATFORM})
        endif($ENV{PLATFORM} STREQUAL "")
    endif(NOT DEFINED ENV{PLATFORM})

    if (${BUILD_PLATFORM} STREQUAL "Win32")
        set (BUILD_PLATFORM "i586")
    endif()

    set (CPACK_PACKAGE_FILE_NAME "operator-${BUILD_PLATFORM}")
    set (CPACK_STRIP_FILES 1)
    set (CPACK_SOURCE_STRIP_FILES 1)
    set (CPACK_CREATE_DESKTOP_LINKS 1)
    set (CPACK_INCLUDE_TOP_LEVEL_DIRECTORY 1)
    set (CPACK_INSTALLED_DIRECTORIES $<TARGET_FILE_DIR:sysmo-operator>/ .)
    set (CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE.txt")
    set (CPACK_PACKAGE_EXECUTABLES sysmo-operator "Sysmo-Operator")

    set (CPACK_GENERATOR WIX)
    set (CPACK_WIX_UPGRADE_GUID "8999771C-F49B-462C-AB3D-CD84432DD585")
    set (CPACK_WIX_PRODUCT_ICON "${CMAKE_CURRENT_SOURCE_DIR}/support/icons/logo.png")

    configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/support/pkgs/win/bundle.wxs
        ${CMAKE_BINARY_DIR}/bundle.wxs)

    configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/support/pkgs/win/bin/build_installer.cmd.in
        ${CMAKE_BINARY_DIR}/build_installer.cmd)


    include(CPack)
endif(WIN32)
