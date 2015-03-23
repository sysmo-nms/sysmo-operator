/* Copyright (C) 2014, Sebastien Serre <sserre.bx@gmail.com>
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
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

package io.sysmo.pyrrd4j;

import java.io.*;
import java.util.*;
import java.nio.file.*;

import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.RejectedExecutionHandler;

import org.rrd4j.core.RrdDef;
import org.rrd4j.core.ArcDef;
import org.rrd4j.core.RrdDb;
import org.rrd4j.core.Sample;
import org.rrd4j.core.FetchData;
import org.rrd4j.core.FetchRequest;
import org.rrd4j.core.RrdDbPool;
import org.rrd4j.graph.RrdGraphDef;
import org.rrd4j.graph.RrdGraph;
import org.rrd4j.DsType;
import org.rrd4j.ConsolFun;
import java.awt.image.BufferedImage;
import java.awt.Color;


class GraphRunnable implements Runnable
{
    private String strArgument;

    public GraphRunnable(String strArg)
    {
        strArgument = strArg.trim();
    }

    @Override
    public void run()
    {
        Pyrrd4j.rrdReply(strArgument);
    }

    public String getArg()
    {
        return strArgument;
    }
}

class UpdateRunnable implements Runnable
{
    private String strArgument;

    public UpdateRunnable(String strArg)
    {
        strArgument = strArg.trim();
    }

    @Override
    public void run()
    {
        Pyrrd4j.rrdReply(strArgument);
    }

    public String getArg()
    {
        return strArgument;
    }
}

public class Pyrrd4j
{
    private static RrdDbPool rrdDbPool = null;
    private static ThreadPoolExecutor threadPool = null;
    private static int threadMaxPoolSize    = 20;
    private static int threadCorePoolSize   = 12;
    private static int threadQueueCapacity  = 3000; // 2 switch of 500 ports X 3 graphs is possible

    // java.exe -classpath java_lib\*; io.sysmo.pyrrd4j.Pyrrd4j --die-on-broken-pipe
    public static void main(String[] args) throws Exception {
        threadPool = new ThreadPoolExecutor(
            threadCorePoolSize,
            threadMaxPoolSize,
            10,
            TimeUnit.MINUTES,
            new ArrayBlockingQueue<Runnable>(threadQueueCapacity),
            new GraphReject()
        );

        rrdDbPool = RrdDbPool.getInstance();
        loopIn();
    }
    
    private static void loopIn()
    {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
            String s;
            while (true) {
                s = in.readLine();
                if (s == null && s.length() == 0) {
                    break;    // An empty line or Ctrl-Z terminates the program
                }
                startWorkder(s);
            }
        }
        catch (Exception|Error e)
        {
            System.exit(1);
            return;
        }
    }

    private static void startWorkder(String arg)
    {
        GraphRunnable   worker = new GraphRunnable(arg);
        threadPool.execute(worker);
    }

    public static synchronized void rrdReply(String reply)
    {
        System.out.println(reply);
    }
}

class GraphReject implements RejectedExecutionHandler
{
    public void rejectedExecution(Runnable r, ThreadPoolExecutor executor)
    {
        GraphRunnable failRunner = (GraphRunnable) r;
        String failArg = failRunner.getArg();
        Pyrrd4j.rrdReply(failArg);
    }
}

