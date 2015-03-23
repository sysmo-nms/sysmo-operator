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
import java.util.Arrays;

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


class RrdRunnable implements Runnable
{
    private String strArgument;
    private String queryId;
    private String reply;

    public RrdRunnable(String line)
    {
        strArgument = line.trim();
    }

    @Override
    public void run()
    {
        
        String[] rrdcmd = strArgument.split(":");

        queryId         = rrdcmd[0];
        String cmdType  = rrdcmd[1];
        String other    = rrdcmd[2];

        int intDebugVal = 0;
        String debugVal = null;
        if (cmdType.equals("GRAPH")) {
            
            String graphCfg[] = other.split(";");
            String title    = graphCfg[0];
            String name     = graphCfg[1];
            String vlabel   = graphCfg[2];
            String rrdFile  = graphCfg[3];
            String pngFile  = graphCfg[4];
            String spanBegin = graphCfg[5];
            String spanEnd  = graphCfg[6];
            String width    = graphCfg[8];
            String height   = graphCfg[9];
            String dsDefs   = graphCfg[10];

            // create graphDef and set elements
             RrdGraphDef graphDef = new RrdGraphDef();
            int spanBeginInt = Integer.parseInt(spanBegin);
            int spanEndInt   = Integer.parseInt(spanEnd);
            graphDef.setTimeSpan(spanBeginInt, spanEndInt);
            graphDef.setTitle(title);
            graphDef.setVerticalLabel(vlabel);
            graphDef.setFilename(pngFile);
            graphDef.setShowSignature(false);

            /*
            graphDef.setColor("BACK", Color.decode("#000000"));
            graphDef.setColor("CANVAS", Color.decode("#000000"));
            graphDef.setColor("SHADEA", Color.decode("#000000"));
            graphDef.setColor("SHADEB", Color.decode("#000000"));
            graphDef.setColor("GRID", Color.decode("#000000"));
            graphDef.setColor("MGRID", Color.decode("#000000"));
            graphDef.setColor("FONT", Color.decode("#000000"));
            graphDef.setColor("FRAME", Color.decode("#000000"));
            graphDef.setColor("ARROW", Color.decode("#000000"));
            */


            // loop over ds and add DS and Line elements
            String[] dsDefList = dsDefs.split("\\@");
            for (String s: dsDefList) {
                dsDefs = s;
                String[] dsD    = s.split(",");
                String dsName   = dsD[0];
                String gType    = dsD[1];
                String gLegend  = dsD[2];
                String gColor   = dsD[3];
                String csFun    = dsD[4];
                ConsolFun csVal = ConsolFun.valueOf(csFun);
                graphDef.datasource(dsName, rrdFile, dsName, csVal);
                
                Color col = Color.decode(gColor);
                if (gType.equals("area")) {
                    graphDef.area(dsName, col, gLegend);
                } else if (gType.equals("line")) {
                    graphDef.line(dsName, col, gLegend, 2);
                }
            }
            int widthInt    = Integer.parseInt(width);
            int heightInt   = Integer.parseInt(height);
            graphDef.setWidth(widthInt);
            graphDef.setHeight(heightInt);

            try {
                RrdGraph graph   = new RrdGraph(graphDef);
                BufferedImage bi = new BufferedImage(100,100,BufferedImage.TYPE_INT_RGB);
                graph.render(bi.getGraphics());
            } catch (Exception|Error e) {
                Pyrrd4j.rrdReply(queryId + ":" + "ERROR:" + e);
                return;
            }
                       
        }
        else if (cmdType.equals("UPDATE")) 
        {
        } 

        Pyrrd4j.rrdReply(queryId + ":OK");
    }

    public String getQueryId()
    {
        return queryId;
    }
}

public class Pyrrd4j
{
    private static RrdDbPool rrdDbPool = null;
    private static ThreadPoolExecutor threadPool = null;
    private static int threadMaxPoolSize    = 20;
    private static int threadCorePoolSize   = 12;
    private static int threadQueueCapacity  = 3000; // 2 switch of 500 ports X 3 graphs

    // java.exe -classpath java_lib\*; io.sysmo.pyrrd4j.Pyrrd4j --die-on-broken-pipe
    public static void main(String[] args) throws Exception {
        threadPool = new ThreadPoolExecutor(
            threadCorePoolSize,
            threadMaxPoolSize,
            10,
            TimeUnit.MINUTES,
            new ArrayBlockingQueue<Runnable>(threadQueueCapacity),
            new RrdReject()
        );

        rrdDbPool = RrdDbPool.getInstance();
        loopIn();
    }
    
    private static void loopIn()
    {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
            String line;
            while (true) {
                line = in.readLine();
                if (line == null && line.length() == 0) {
                    break;    // An empty line or Ctrl-Z terminates the program
                }
                startWorkder(line);
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
        RrdRunnable   worker = new RrdRunnable(arg);
        threadPool.execute(worker);
    }

    public static synchronized void rrdReply(String reply)
    {
        System.out.println(reply);
    }
}

class RrdReject implements RejectedExecutionHandler
{
    public void rejectedExecution(Runnable r, ThreadPoolExecutor executor)
    {
        RrdRunnable failRunner = (RrdRunnable) r;
        String queryId = failRunner.getQueryId();
        Pyrrd4j.rrdReply(queryId + ":ERROR:Max thread queue reached");
    }
}

