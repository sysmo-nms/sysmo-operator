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
import org.rrd4j.graph.RrdGraphConstants;
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
    private String cmdArgs;
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
        cmdArgs         = rrdcmd[2];

        int intDebugVal = 0;
        String debugVal = null;
        switch (cmdType)
        {
            case "GRAPH":
                handleGraph();
                break;
            case "UPDATE":
                handleUpdate();
                break;
            case "CONFIG":
                handleConfig();
                break;
            default:
                Pyrrd4j.rrdReply(queryId + ":ERROR");
        }
    }

                
    private void handleConfig()
    {
        String colorCfg[] = cmdArgs.split(";");
        CustomRrdGraphDef.BACK_C      = Color.decode(colorCfg[0]);
        CustomRrdGraphDef.CANVAS_C    = Color.decode(colorCfg[1]);
        CustomRrdGraphDef.SHADEA_C    = Color.decode(colorCfg[2]);
        CustomRrdGraphDef.SHADEB_C    = Color.decode(colorCfg[3]);
        CustomRrdGraphDef.GRID_C      = Color.decode(colorCfg[4]);
        CustomRrdGraphDef.MGRID_C     = Color.decode(colorCfg[5]);
        CustomRrdGraphDef.FONT_C      = Color.decode(colorCfg[6]);
        CustomRrdGraphDef.FRAME_C     = Color.decode(colorCfg[7]);
        CustomRrdGraphDef.ARROW_C     = Color.decode(colorCfg[8]);
        CustomRrdGraphDef.XAXIS_C     = Color.decode(colorCfg[9]);
        Pyrrd4j.rrdReply(queryId + ":OK" + cmdArgs);
    }
    
    private void handleUpdate()
    {
    }

    private void handleGraph()
    {
        String graphCfg[] = cmdArgs.split(";");
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
        CustomRrdGraphDef graphDef = new CustomRrdGraphDef();
        int spanBeginInt = Integer.parseInt(spanBegin);
        int spanEndInt   = Integer.parseInt(spanEnd);
        graphDef.setTimeSpan(spanBeginInt, spanEndInt);
        graphDef.setTitle(title);
        graphDef.setVerticalLabel(vlabel);
        graphDef.setFilename(pngFile);
        graphDef.setShowSignature(false);



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
        Pyrrd4j.rrdReply(queryId + ":OK");
    }


    public String getQueryId()
    {
        return queryId;
    }

}


class CustomRrdGraphDef extends RrdGraphDef
{        
    public static Color BACK_C;
    public static Color CANVAS_C;
    public static Color SHADEA_C;
    public static Color SHADEB_C;
    public static Color GRID_C;
    public static Color MGRID_C;
    public static Color FONT_C;
    public static Color FRAME_C;
    public static Color ARROW_C;
    public static Color XAXIS_C;

    public CustomRrdGraphDef()
    {
        super();
        this.setColor(RrdGraphConstants.COLOR_BACK,   BACK_C);
        this.setColor(RrdGraphConstants.COLOR_CANVAS, CANVAS_C);
        this.setColor(RrdGraphConstants.COLOR_SHADEA, SHADEA_C);
        this.setColor(RrdGraphConstants.COLOR_SHADEB, SHADEB_C);
        this.setColor(RrdGraphConstants.COLOR_GRID,   GRID_C);
        this.setColor(RrdGraphConstants.COLOR_MGRID,  MGRID_C);
        this.setColor(RrdGraphConstants.COLOR_FONT,   FONT_C);
        this.setColor(RrdGraphConstants.COLOR_FRAME,  FRAME_C);
        this.setColor(RrdGraphConstants.COLOR_ARROW,  ARROW_C);
        this.setColor(RrdGraphConstants.COLOR_XAXIS,  XAXIS_C);
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

