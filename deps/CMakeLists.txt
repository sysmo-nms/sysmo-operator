# CLOG is header only
set(DEPS_INCLUDES "${CMAKE_CURRENT_SOURCE_DIR}/clog/")

# CARGO is header only
set(DEPS_INCLUDES ${DEPS_INCLUDES} "${CMAKE_CURRENT_SOURCE_DIR}/cargo/")

# RRDIO is a Java project built with Gradle
if (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
    set (GRADLE_BIN ${CMAKE_CURRENT_SOURCE_DIR}/rrdio/gradlew.bat)
else ()
    set (GRADLE_BIN ${CMAKE_CURRENT_SOURCE_DIR}/rrdio/gradlew)
endif (${CMAKE_SYSTEM_NAME} MATCHES "Windows")
execute_process(
    COMMAND ${GRADLE_BIN} installDist
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/rrdio
    OUTPUT_QUIET)

# return
set(OPERATOR_DEPS_INCLUDES  ${DEPS_INCLUDES} PARENT_SCOPE)
set(OPERATOR_DEPS_LIBRARIES ${DEPS_LIBRARIES} PARENT_SCOPE)
