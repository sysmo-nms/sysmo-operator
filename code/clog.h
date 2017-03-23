/*
 * MIT License
 *
 * CLOG Copyright (c) 2016 Sebastien Serre <ssbx@sysmo.io>.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/**
 * @file clog.h
 * @brief Logging utility.
 */

#ifndef CLOG_H
#define CLOG_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <time.h>

/**
 * @mainpage
 * See clog.h for documentation.
 */



/**
 * @def clogError(format, args ...)
 * Log an error message. Format and args are similar to the printf() function
 * @param format format send to printf
 * @param args variable size arguments send to printf or NULL if undefined
 */
#define clogError(format, args, ...) {\
    clogLog("ERROR", __FILE__, __LINE__, format, args);\
}


/**
 * @def clogWarning(format, args ...)
 * Log a warning message. Format and args are similar to the printf() function
 * @param format format send to printf
 * @param args variable size arguments send to printf or NULL.
 */
#define clogWarning(format, args, ...) {\
    clogLog("WARNING", __FILE__, __LINE__, format, args);\
}


/**
 * @def clogInfo(format, args ...)
 * Log a info message. Format and args are similar to the printf() function
 * @param format format send to printf
 * @param args variable size arguments send to printf or NULL.
 */
#define clogInfo(format, args, ...) {\
    clogLog("INFO", __FILE__, __LINE__, format, args);\
}


/**
 * @def clogDebug(format, args ...)
 * Log a debug message. Format and args are similar to the printf() function
 * @param format format send to printf
 * @param args variable size arguments send to printf or NULL.
 */
#ifdef CLOG_DEBUG
#define clogDebug(format, args, ...) {\
    clogLog("DEBUG", __FILE__, __LINE__, format, args);\
}
#else
#define clogDebug(format, ...) {}
#endif

FILE* CLOG_OUT;


#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

/**
 * @brief For internal use only.
 */
static void clogTerminate()
{

    if (NULL != CLOG_OUT) fclose(CLOG_OUT);

}


/**
 * @brief Specify a file insteed of STDOUT to log messages.
 * Set filePath as the destination for logs.
 * @param filepath the full file name to write on.
 * @returns 0 if succeed, 1 if the file cannot be opened.
 */
static int clogConfigure(const char* filepath)
{

    atexit(clogTerminate);

    if (NULL != CLOG_OUT) fclose(CLOG_OUT);

    FILE* logFile = fopen(filepath, "a");

    if (NULL == logFile)
        return 1;
    else
        CLOG_OUT = logFile;

    return 0;

}

/**
 * @brief For internal use only.
 */
static int clogLog(
        char* level,
        char* file,
        int   line,
        const char* format, ...)
{


    FILE* out;
    if (NULL != CLOG_OUT) {

        out = CLOG_OUT;

    } else {

        out = stdout;

    }

    time_t timer;
    time(&timer);

    char timeBuffer[30];
    strftime(timeBuffer, 30, "%Y/%m/%d %H:%M:%S", localtime(&timer));

    fprintf(out, "\n\n%s\t%s\t%s:%d\n", timeBuffer, level, file, line); 


    va_list args;
    int ret;

    va_start(args, format);
    ret = vfprintf(out, format, args);
    va_end(args);

    return ret;

}

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // CLOG_H

