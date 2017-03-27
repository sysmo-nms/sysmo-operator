#include <clog.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <time.h>

FILE* CLOG_OUTPUT = NULL;

static void clogTerminate()
{

    if (NULL != CLOG_OUTPUT) fclose(CLOG_OUTPUT);

}

void
clogSetOutputFd(FILE *fd)
{
    CLOG_OUTPUT = fd;
}

void *
clogSetOutput(const char* filepath)
{

    atexit(clogTerminate);

    if (NULL != CLOG_OUTPUT) fclose(CLOG_OUTPUT);

    FILE* logFile = fopen(filepath, "a");

    if (NULL == logFile)
        CLOG_OUTPUT = NULL;
    else
        CLOG_OUTPUT = logFile;

    return CLOG_OUTPUT;

}

int clogLog(
        const char* level,
        const char* file,
        int line,
        const char* format, ...)
{

    if (CLOG_OUTPUT == NULL)
        return -1;

    time_t timer;
    time(&timer);

    char timeBuffer[30];
    strftime(timeBuffer, 30, "%Y/%m/%d %H:%M:%S", localtime(&timer));

    fprintf(CLOG_OUTPUT, "\n\n%s\t%s\t%s:%d\n", timeBuffer, level, file, line);

    va_list args;
    int ret;

    va_start(args, format);
    ret = vfprintf(CLOG_OUTPUT, format, args);
    va_end(args);

    return ret;

}


