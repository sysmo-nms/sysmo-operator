#
# RRDIO is a Java project built with Gradle
# Get all dependencies
file(GLOB RRD4J_JAR_FULL rrdio/build/install/rrdio/lib/rrd4j*.jar)
get_filename_component(RRD4J_JAR ${RRD4J_JAR_FULL} NAME)

file(GLOB RRDIO_JAR_FULL rrdio/build/install/rrdio/lib/rrdio*.jar)
get_filename_component(RRDIO_JAR ${RRDIO_JAR_FULL} NAME)

file(GLOB JSON_JAR_FULL  rrdio/build/install/rrdio/lib/javax.json*.jar)
get_filename_component(JSON_JAR ${JSON_JAR_FULL} NAME)

set(RRDIO_JAR       ${RRDIO_JAR} CACHE INTERNAL STRING)
set(RRDIO_RRD4J_JAR ${RRD4J_JAR} CACHE INTERNAL STRING)
set(RRDIO_JSON_JAR  ${JSON_JAR}  CACHE INTERNAL STRING)

