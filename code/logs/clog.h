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

extern FILE* CLOG_OUTPUT;

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

    /**
     * @brief Specify a file to log messages.
     * Set filePath as the destination for logs.
     * @param filepath the full file name to write on.
     * @returns the file descriptor or NULL if failed (see errno).
     */
    void* clogSetOutput(const char* filepath);

    /**
     * @brief Specify a file descriptor to log messages, or NULL to disable
     * logs.
     * @param fd a FILE*
     */
    void clogSetOutputFd(FILE *fd);


    /**
     * @brief For internal use only.
     */
    int clogLog(
            const char* level,
            const char* file,
            int line,
            const char* format, ...);

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // CLOG_H

