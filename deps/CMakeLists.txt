# CLOG is header only
set(DEPS_INCLUDES "${CMAKE_CURRENT_SOURCE_DIR}/clog/")

# CARGO is header only
set(DEPS_INCLUDES ${DEPS_INCLUDES} "${CMAKE_CURRENT_SOURCE_DIR}/cargo/")

# PARSON
set(DEPS_INCLUDES ${DEPS_INCLUDES} "${CMAKE_CURRENT_SOURCE_DIR}/parson/")
add_library(parson parson/parson.c parson/parson.h)
set(DEPS_LIBRARIES parson)

# XMLC 
set(DEPS_INCLUDES ${DEPS_INCLUDES} "${CMAKE_CURRENT_SOURCE_DIR}/xmlc/src/")
add_library(xml xmlc/src/xml.c xmlc/src/xml.h)
set(DEPS_LIBRARIES ${DEPS_LIBRARIES} xml)



# return
set(OPERATOR_DEPS_INCLUDES  ${DEPS_INCLUDES} PARENT_SCOPE)
set(OPERATOR_DEPS_LIBRARIES ${DEPS_LIBRARIES} PARENT_SCOPE)
