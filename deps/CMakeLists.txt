#
# CLOG is header only
#
set(DEPS_INCLUDES "${CMAKE_CURRENT_SOURCE_DIR}/clog/")


#
# CARGO is header only
#
set(DEPS_INCLUDES ${DEPS_INCLUDES} "${CMAKE_CURRENT_SOURCE_DIR}/cargo/")

#
# qjson
#
add_subdirectory(qjson)
set(DEPS_INCLUDES ${DEPS_INCLUDES} "${CMAKE_CURRENT_SOURCE_DIR}/qjson/")
set(DEPS_LIBRARIES qjson)

#
# RRDIO is a Java project built with Gradle
#
# Build it:
if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set (GRADLE_BIN ${CMAKE_CURRENT_SOURCE_DIR}/rrdio/gradlew.bat)
else ()
    set (GRADLE_BIN ${CMAKE_CURRENT_SOURCE_DIR}/rrdio/gradlew)
endif (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
message(STATUS "Preparing Java RrdIO...")
execute_process(
    COMMAND ${GRADLE_BIN} installDist
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/rrdio)
message(STATUS "Java RrdIO Ready")

# Get all dependencies
file(GLOB RRD4J_JAR_FULL rrdio/build/install/rrdio/lib/rrd4j*.jar)
get_filename_component(RRD4J_JAR ${RRD4J_JAR_FULL} NAME)

file(GLOB RRDIO_JAR_FULL rrdio/build/install/rrdio/lib/rrdio*.jar)
get_filename_component(RRDIO_JAR ${RRDIO_JAR_FULL} NAME)

file(GLOB JSON_JAR_FULL  rrdio/build/install/rrdio/lib/javax.json*.jar)
get_filename_component(JSON_JAR ${JSON_JAR_FULL} NAME)

#
# return
#
set(OPERATOR_DEPS_INCLUDES  ${DEPS_INCLUDES} PARENT_SCOPE)
set(OPERATOR_DEPS_LIBRARIES ${DEPS_LIBRARIES} PARENT_SCOPE)
set(RRDIO_JAR       ${RRDIO_JAR} PARENT_SCOPE)
set(RRDIO_RRD4J_JAR ${RRD4J_JAR} PARENT_SCOPE)
set(RRDIO_JSON_JAR  ${JSON_JAR} PARENT_SCOPE)

