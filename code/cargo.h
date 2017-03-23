/*
 * MIT License
 *
 * CARGO Copyright (c) 2016 Sebastien Serre <ssbx@sysmo.io>.
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
 * @mainpage
 * 
 * <a target="_blank" href="https://github.com/libgame/cargo">See CARGO on GitHub</a>.
 *
 * @section Usage
 * See the documentation for the cargoFlag() function.
 *
 * @section Example
 * To handle the following program arguments:
 * @code
 * ./myprog --flag1 --flag3= --flag4="Hello world"
 * @endcode
 * 
 * You could write this:
 * @code
 *
 * [...]
 *
 * int main(int argc, char* argv[])
 * {
 *
 *     char* f1 = cargoFlag("flag1", "FALSE",      argc, argv); // f1 = "TRUE"
 *     char* f2 = cargoFlag("flag2", "FALSE",      argc, argv); // f2 = "FALSE"
 *     char* f3 = cargoFlag("flag3", "defaultval", argc, argv); // f3 = ""
 *     char* f4 = cargoFlag("flag4", "Bye world",  argc, argv); // f4 = "Hello world"
 *     char* f5 = cargoFlag("flag5", "Bye world",  argc, argv); // f5 = "Bye world"
 * 
 * }
 * @endcode
 */

/**
 * @file cargo.h
 */
#ifndef CARGO_H
#define CARGO_H

#include <string.h>
#include <stdlib.h>

#define FLAG_MAX_SIZE 80
#define FLAG_MAX_NUMBER 20

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

static char** CARGO_allocated_args;
static int    CARGO_initialized = 0;
static int    CARGO_current_arg;

static void cargoCleanup()
{

    if (CARGO_initialized == 0) return;
    if (CARGO_current_arg == 0) return;

    int i;
    for (i=0; i < CARGO_current_arg; i++)
    {
        free(CARGO_allocated_args[i]);
    }

    free(CARGO_allocated_args);

}

static void cargoInit()
{

    if (CARGO_initialized == 1) return;

    CARGO_allocated_args = (char**) malloc(sizeof(char*) * FLAG_MAX_NUMBER);
    CARGO_current_arg = 0;
    atexit(&cargoCleanup);
    CARGO_initialized = 1;

}

/**
 * @brief Get the content of a flag if it is an assignment flag (--myflag=),
 * the string "TRUE" if the flag is defined as boolean (--myflag)
 * or the default value if neither assignment or boolean flag is defined.
 *
 * If the flag is defined multiple time, as boolean or assignment, the value of
 * the last flag occurence is returned.
 *
 * @param flag The flag name
 *
 * @param defaultValue The default value if the flag is not found
 *
 * @param argc The original main(argc,_) value
 *
 * @param argv The original main(_,argv) value
 *
 * @return A pointer to a char array. It is up to the user to free() this array. 
 */
static char* cargoFlag(
        char*  name, 
        char*  defaultValue,
        int    argc,
        char** argv)
{

    cargoInit();

    // generate the flag name
    char flagName[FLAG_MAX_SIZE];
    strcpy(&flagName[0], "--");
    strcpy(&flagName[2], name);
    strcpy(&flagName[strlen(name) + 2], "=");

    // return value
    char* content = NULL;

    // iterate over argv
    int j;
    for (j = 0; j < argc; j++)
    {

        char* arg = argv[j];

        if (strncmp(flagName, arg, strlen(flagName)) == 0)
        { // flag found with "="

            if (strlen(flagName) == strlen(arg)) // no content
            {

                if (content != NULL) free(content);
                content = (char*) malloc(1);
                *content = '\0';

                continue;

            }

            // there is some content
            if (content != NULL) free(content);
            content = (char*) malloc(strlen(arg) - strlen(flagName) + 1);
            strcpy(content, &arg[strlen(flagName)]);

        }
        else if (strncmp(flagName, arg, strlen(flagName) - 1) == 0)
        { // found partial flag --${name}

            // set content to true if it is the end of the str
            if (strlen(arg) == strlen(flagName) -1)
            {

                if (content != NULL) free(content);
                content = (char*) malloc(strlen("TRUE") + 1);
                strcpy(content, "TRUE");

            }
        }
    }

    if (content == NULL)
    { // flag not found set default

        content = (char*) malloc(strlen(defaultValue) + 1);
        strcpy(content, defaultValue);

    }

    CARGO_allocated_args[CARGO_current_arg] = content;
    CARGO_current_arg += 1;

    return content;

}

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // CARGO_H

