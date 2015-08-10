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
 * FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

package io.sysmo.rrd4qt;

import java.io.*;
import java.nio.ByteBuffer;

import java.util.Set;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.RejectedExecutionHandler;

import java.util.logging.Logger;
import java.util.logging.Level;

import org.rrd4j.core.RrdDb;
import org.rrd4j.core.RrdDbPool;
import org.rrd4j.core.Sample;
import org.rrd4j.graph.RrdGraph;
import org.rrd4j.graph.RrdGraphConstants;
import org.rrd4j.graph.RrdGraphDef;
import org.rrd4j.ConsolFun;

import java.awt.Color;

import javax.imageio.ImageIO;

import javax.json.Json;
import javax.json.JsonValue;
import javax.json.JsonArray;
import javax.json.JsonReaderFactory;
import javax.json.JsonObject;

/**
 * Created by Sebastien Serre on 09/07/15
 */

public class Rrd4Qt
{
    private static ThreadPoolExecutor threadPool = null;
    private static OutputStream       out        = null;
    public  static RrdDbPool          rrdDbPool  = null;
    public  static Logger             logger     = null;

    public static void main(String[] args) throws Exception
    {
        /*
         * Init logger (default ConsoleLogger to System.err).
         */
        Rrd4Qt.logger = Logger.getLogger("rrd4qt");
        Rrd4Qt.logger.setLevel(Level.ALL);

        /*
         * Disable disk caching for ImageIO
         */
        ImageIO.setUseCache(false);

        /*
         * init thread pool and rrdDbPool
         */
        Rrd4Qt.rrdDbPool  = RrdDbPool.getInstance();
        Rrd4Qt.threadPool = new ThreadPoolExecutor(
            12, //thread Core Pool Size
            20, //thread Max Pool Size
            10,
            TimeUnit.MINUTES,
            new ArrayBlockingQueue<>(3000), // 3000 = queue capacity
            new RrdReject()
        );

        /*
         * initialize out
         */
        Rrd4Qt.out = System.out;

        /*
         * Begin loop listen System.in
         */
        try {
            InputStream in = System.in;
            byte[]  header = new byte[4];
            byte[]  buffer = new byte[65535];
            int     size;
            int     read;
            int     status;
            JsonReaderFactory    readerFactory = Json.createReaderFactory(null);
            JsonObject           jsonObject;
            ByteArrayInputStream inStream;
            Rrd4QtJob            rrdWorker;

            while (true) {
                /*
                 * Get the first byte (as int 0 to 255 or -1 if EOF)
                 */
                status = in.read();
                if (status == -1) throw new IOException("STDIN broken");

                /*
                 * Complete the header[4]
                 */
                header[0] = (byte)status;
                header[1] = (byte)in.read();
                header[2] = (byte)in.read();
                header[3] = (byte)in.read();

                /*
                 * Compute the size of the message
                 */
                size = ByteBuffer.wrap(header, 0, 4).getInt();

                /*
                 *Now we can read the message
                 */
                read = 0;
                while (read != size)
                    read += in.read(buffer, read, size - read);

                /*
                 * Create a json object from the buffer
                 */
                inStream   = new ByteArrayInputStream(buffer, 0, size);
                jsonObject = readerFactory.createReader(inStream).readObject();

                /*
                 * Start Rrd4QtJob
                 */
                rrdWorker = new Rrd4QtJob(jsonObject);
                Rrd4Qt.threadPool.execute(rrdWorker);
            }
        }
        catch (Exception e)
        {
            Rrd4Qt.logger.log(Level.SEVERE, e.toString());
            System.exit(1);
        }
    }

    public static synchronized void rrdReply(JsonObject object)
    {
        try {
            ByteBuffer b = ByteBuffer.allocate(4);
            byte[] reply = object.toString().getBytes();
            b.putInt(reply.length);

            Rrd4Qt.out.write(b.array(), 0, 4);
            Rrd4Qt.out.write(reply,     0, reply.length);
            Rrd4Qt.out.flush();
        }
        catch (Exception e)
        {
            Rrd4Qt.logger.log(Level.SEVERE, e.toString());
        }
    }

    public static Color decodeRGBA(String hexString)
    {
        return new Color(
                Integer.valueOf(hexString.substring(1,3), 16),
                Integer.valueOf(hexString.substring(3,5), 16),
                Integer.valueOf(hexString.substring(5,7), 16),
                Integer.valueOf(hexString.substring(7,9), 16)
        );
    }
}


class RrdReject implements RejectedExecutionHandler
{
    public void rejectedExecution(Runnable r, ThreadPoolExecutor executor)
    {
        Rrd4QtJob failRunner = (Rrd4QtJob) r;
        int      queryId = failRunner.getQueryId();
        JsonObject reply = Json.createObjectBuilder()
                .add("queryId", queryId)
                .add("reply", "Error thread queue full!")
                .build();
        Rrd4Qt.rrdReply(reply);
    }
}

class Rrd4QtGraphDef extends RrdGraphDef
{
    private static Color BACK_C;
    private static Color CANVAS_C;
    private static Color SHADEA_C;
    private static Color SHADEB_C;
    private static Color GRID_C;
    private static Color MGRID_C;
    private static Color FONT_C;
    private static Color FRAME_C;
    private static Color ARROW_C;
    private static Color XAXIS_C;

    public Rrd4QtGraphDef()
    {
        super(); // RrdGraphDef()
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
        this.setImageFormat("png");
        this.setShowSignature(false);
        this.setAntiAliasing(true);
        this.setTextAntiAliasing(true);
        this.setImageQuality((float) 1.0);
        this.setLazy(false);
        //this.setFontSet(true);
    }

    public static void setDefaultColors(JsonObject colorCfg)
    {
        JsonObject col;
        col = colorCfg.getJsonObject("BACK");
        Rrd4QtGraphDef.BACK_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));

        col = colorCfg.getJsonObject("CANVAS");
        Rrd4QtGraphDef.CANVAS_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));

        col = colorCfg.getJsonObject("SHADEA");
        Rrd4QtGraphDef.SHADEA_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));

        col = colorCfg.getJsonObject("SHADEB");
        Rrd4QtGraphDef.SHADEB_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));

        col = colorCfg.getJsonObject("GRID");
        Rrd4QtGraphDef.GRID_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));

        col = colorCfg.getJsonObject("MGRID");
        Rrd4QtGraphDef.MGRID_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));

        col = colorCfg.getJsonObject("FONT");
        Rrd4QtGraphDef.FONT_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));

        col = colorCfg.getJsonObject("FRAME");
        Rrd4QtGraphDef.FRAME_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));

        col = colorCfg.getJsonObject("ARROW");
        Rrd4QtGraphDef.ARROW_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));

        col = colorCfg.getJsonObject("XAXIS");
        Rrd4QtGraphDef.XAXIS_C =
                new Color(col.getInt("red"), col.getInt("green"),
                        col.getInt("blue"), col.getInt("alpha"));
    }
}


class Rrd4QtJob implements Runnable
{
    private JsonObject job;

    public Rrd4QtJob(JsonObject job) { this.job = job; }

    public int getQueryId() { return this.job.getInt("queryId"); }

    @Override
    public void run()
    {
        Rrd4Qt.logger.log(Level.INFO, this.job.toString());

        String cmdType = this.job.getString("type");
        switch (cmdType)
        {
            case "graph":
                this.handleGraph();
                break;
            case "update":
                this.handleUpdate();
                break;
            case "color_config":
                this.handleConfig();
                break;
            default:
                Rrd4Qt.logger.log(Level.SEVERE, "Unknown command: " + cmdType);
        }
    }

    private void handleConfig()
    {
        Rrd4QtGraphDef.setDefaultColors(this.job);
    }

    private void handleUpdate()
    {
        /*
         * get arguments
         */
        String    rrdFile = this.job.getString("file");
        long    timestamp = (long)this.job.getInt("timestamp");
        JsonObject update = this.job.getJsonObject("updates");
        String     opaque = this.job.getString("opaque");
        int       queryId = this.job.getInt("queryId");

        String replyStatus;

        /*
         * open and write rrd db
         */
        try {
            RrdDb   rrdDb = Rrd4Qt.rrdDbPool.requestRrdDb(rrdFile);
            Sample sample = rrdDb.createSample();
            sample.setTime(timestamp);

            Set<String> updateKeys = update.keySet();
            for (String key : updateKeys)
                sample.setValue(key, (long) update.getInt(key));

            sample.update();
            Rrd4Qt.rrdDbPool.release(rrdDb);
            replyStatus = "success";

        } catch (Exception e) {
            Rrd4Qt.logger.log(Level.SEVERE, e.toString());
            replyStatus = "failure";
        }

        /*
         * Build and send reply
         */
        JsonObject reply = Json.createObjectBuilder()
                .add("reply",   replyStatus)
                .add("opaque",  opaque)
                .add("queryId", queryId)
                .build();
        Rrd4Qt.rrdReply(reply);
    }

    private void handleGraph()
    {
        /*
         * Get logical arguments
         */
        String opaque = this.job.getString("opaque");
        int   queryId = this.job.getInt("queryId");

        /*
         * Get graph arguments
         */
        String rrdFile = this.job.getString("rrdFile");
        String pngFile = this.job.getString("pngFile");

        String title  = this.job.getString("title");
        String vlabel = this.job.getString("verticalLabel");

        int spanBegin = this.job.getInt("spanBegin");
        int spanEnd   = this.job.getInt("spanEnd");

        int width  = this.job.getInt("width");
        int height = this.job.getInt("height");

        String minVal = this.job.getString("minimum");
        String maxVal = this.job.getString("maximum");

        String rigid   = this.job.getString("rigid");
        String base    = this.job.getString("base");
        String unit    = this.job.getString("unit");
        String unitExp = this.job.getString("unitExponent");

        /*
         * Generate the graph definition.
         */
        Rrd4QtGraphDef graphDef = new Rrd4QtGraphDef();
        graphDef.setTimeSpan(spanBegin, spanEnd);
        graphDef.setTitle(title);
        graphDef.setVerticalLabel(vlabel);
        graphDef.setFilename(pngFile);
        graphDef.setImageFormat("png");
        graphDef.setBase(Double.parseDouble(base));
        graphDef.setWidth(width);
        graphDef.setHeight(height);

        if (rigid.equals("true")) {
            graphDef.setRigid(true);
        }

        if (!unit.equals("")) {
            graphDef.setUnit(unit);
        }

        if (!unitExp.equals("")) {
            try {
                int unitExpInt = Integer.parseInt(unitExp);
                graphDef.setUnitsExponent(unitExpInt);
            } catch (Exception e) {
                Rrd4Qt.logger.log(
                        Level.INFO, "bad unit exp: " + unitExp + e.toString());
            }
        }

        if (!minVal.equals("")) {
            try {
                double minValDouble = Double.parseDouble(minVal);
                graphDef.setMinValue(minValDouble);
            } catch (Exception e) {
                Rrd4Qt.logger.log(
                        Level.INFO, "min val not a double: " + e.toString());
            }
        }

        if (!maxVal.equals("")) {
            try {
                double maxValDouble = Double.parseDouble(maxVal);
                graphDef.setMaxValue(maxValDouble);
            } catch (Exception e) {
                Rrd4Qt.logger.log(
                        Level.INFO, "max val not a double: " + e.toString());
            }
        }

        /*
         * Get DS Draw list and iterate.
         */
        JsonArray dataSources = this.job.getJsonArray("draws");
        for(JsonValue ds : dataSources)
        {
            JsonObject obj = (JsonObject)ds;
            String    dsName   = obj.getString("dataSource");
            String    dsColor  = obj.getString("color");
            String    dsLegend = obj.getString("legend");
            String    dsType   = obj.getString("type");
            String    calc     = obj.getString("calculation");

            Color     color = Rrd4Qt.decodeRGBA(dsColor);
            ConsolFun dsCons = ConsolFun.valueOf(
                    obj.getString("consolidation"));

            graphDef.datasource(dsName, rrdFile, dsName, dsCons);

            String drawName;
            if (calc.equals("")) {
                drawName = dsName;
            } else {
                drawName = "calculation-" + dsName;
                graphDef.datasource(drawName, calc);
            }

            switch (dsType)
            {
                case "area":
                    graphDef.area(drawName, color, dsLegend);
                    break;
                case "stack":
                    graphDef.stack(drawName, color, dsLegend);
                    break;
                default:
                    graphDef.line(drawName, color, dsLegend);
            }
        }

        /*
         * Graph:
         */
        String replyStatus;
        try {
            new RrdGraph(graphDef);
            replyStatus = "success";

        } catch (Exception e) {
            Rrd4Qt.logger.log(
                    Level.WARNING, "fail to generate graph: " + e.toString());
            replyStatus = "failure";
        }

        /*
         * Build and send reply
         */
        Rrd4Qt.logger.log(Level.INFO, dataSources.toString());
        JsonObject reply = Json.createObjectBuilder()
                .add("reply",   replyStatus)
                .add("opaque",  opaque)
                .add("queryId", queryId)
                .build();
        Rrd4Qt.rrdReply(reply);
    }
}
