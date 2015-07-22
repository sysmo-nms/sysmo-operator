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
import org.rrd4j.graph.RrdGraphConstants;
import org.rrd4j.graph.RrdGraphDef;
import org.rrd4j.ConsolFun;

import java.awt.Color;

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
         * initialize out and json reader
         */
        Rrd4Qt.out = System.out;
        JsonReaderFactory readerFactory = Json.createReaderFactory(null);

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
                ByteArrayInputStream reader =
                        new ByteArrayInputStream(buffer, 0, size);
                JsonObject jsonObject =
                        readerFactory.createReader(reader).readObject();

                /*
                 * Start Rrd4QtJob
                 */
                Rrd4QtJob worker = new Rrd4QtJob(jsonObject);
                Rrd4Qt.threadPool.execute(worker);
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
        this.setImageFormat("png");
        this.setShowSignature(false);
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
    private JsonObject command;

    public Rrd4QtJob(JsonObject job) { this.command = job; }

    public int getQueryId() { return this.command.getInt("queryId"); }

    @Override
    public void run()
    {
        Rrd4Qt.logger.log(Level.INFO, this.command.toString());

        String cmdType = this.command.getString("type");
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
        Rrd4QtGraphDef.setDefaultColors(this.command);
    }

    private void handleUpdate()
    {
        /*
         * get arguments
         */
        String    rrdFile = this.command.getString("file");
        long    timestamp = (long)this.command.getInt("timestamp");
        JsonObject update = this.command.getJsonObject("updates");
        String     opaque = this.command.getString("opaque");
        int       queryId = this.command.getInt("queryId");

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
        String opaque = this.command.getString("opaque");
        int   queryId = this.command.getInt("queryId");

        /*
         * Get graph arguments
         */
        String rrdFile = this.command.getString("rrdFile");
        String pngFile = this.command.getString("pngFile");

        String title  = this.command.getString("title");
        String vlabel = this.command.getString("verticalLabel");

        int spanBegin = this.command.getInt("spanBegin");
        int spanEnd   = this.command.getInt("spanEnd");

        int width  = this.command.getInt("width");
        int height = this.command.getInt("height");

        String minVal = this.command.getString("minimum");
        String maxVal = this.command.getString("maximum");

        String rigid   = this.command.getString("rigid");
        String base    = this.command.getString("base");
        String unit    = this.command.getString("unit");
        String unitExp = this.command.getString("unitExponent");

        /*
         * Generate the graph definition.
         */
        Rrd4QtGraphDef graphDef = new Rrd4QtGraphDef();
        graphDef.setTimeSpan(spanBegin, spanEnd);
        graphDef.setTitle(title);
        graphDef.setVerticalLabel(vlabel);
        graphDef.setFilename(pngFile);
        graphDef.setBase(Double.parseDouble(base));
        graphDef.setUnit(unit);
        graphDef.setUnitsExponent(Integer.parseInt(unitExp));

        try {
            double minValDouble = Double.parseDouble(minVal);
            graphDef.setMinValue(minValDouble);
        } catch (Exception e) {
            Rrd4Qt.logger.log(Level.INFO, "min val not a double: " + e.toString());
        }

        try {
            double maxValDouble = Double.parseDouble(maxVal);
            graphDef.setMaxValue(maxValDouble);
        } catch (Exception e) {
            Rrd4Qt.logger.log(Level.INFO, "max val not a double: " + e.toString());
        }

        if (rigid.equals("true")) graphDef.setRigid(true);


        /*
         * Get DS Draw list
         */
        JsonArray dataSources = this.command.getJsonArray("draws");
        for(JsonValue ds : dataSources)
        {
            JsonObject obj = (JsonObject)ds;
            String    dsName   = obj.getString("dataSource");
            String    dsColor  = obj.getString("color");
            String    dsLegend = obj.getString("legend");
            String    dsType   = obj.getString("type");
            ConsolFun dsCons   = ConsolFun.valueOf(
                                                obj.getString("consolidation"));

            graphDef.datasource(dsName, rrdFile, dsName, dsCons);
        }

        Rrd4Qt.logger.log(Level.INFO, dataSources.toString());

        JsonObject reply = Json.createObjectBuilder()
                .add("reply",   "ok")
                .add("opaque",  opaque)
                .add("queryId", queryId)
                .build();
        Rrd4Qt.rrdReply(reply);
    }
}
