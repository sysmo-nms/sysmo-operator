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

package io.sysmo.rrd4qt;

import java.io.OutputStreamWriter;
import java.nio.ByteBuffer;
import java.io.InputStreamReader;
import java.io.IOException;



import java.nio.charset.Charset;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.RejectedExecutionHandler;

import org.rrd4j.core.RrdDbPool;
import java.awt.Color;


public class Rrd4Qt
{
    public  static RrdDbPool          rrdDbPool    = null;
    private static ThreadPoolExecutor threadPool   = null;
    private static OutputStreamWriter outputStream = null;

    public static void main(String[] args) throws Exception
    {

        /*
         * Catch kill
         */
        Runtime.getRuntime().addShutdownHook(
            new Thread() {
                @Override
                public void run() {}
            }
        );

        Rrd4Qt.rrdDbPool  = RrdDbPool.getInstance();
        Rrd4Qt.threadPool = new ThreadPoolExecutor(
            12, //thread Core Pool Size
            20, //thread Max Pool Size
            10,
            TimeUnit.MINUTES,
            new ArrayBlockingQueue<>(3000), // 3000 = queue capacity
            new RrdReject()
        );

        Rrd4Qt.outputStream = new OutputStreamWriter(System.out, Charset.forName("US-ASCII"));
        try {
            InputStreamReader in = new InputStreamReader(System.in, Charset.forName("US-ASCII"));
            byte[] header = new byte[4];
            char[] buffer = new char[1024];
            int size;
            int read;
            while (true) {
                header[0] = (byte)in.read();
                if (header[0] == -1) throw new IOException("End of stream");
                header[1] = (byte)in.read();
                header[2] = (byte)in.read();
                header[3] = (byte)in.read();

                size = ByteBuffer.wrap(header).getInt();
                read = 0;
                while (read != size) read += in.read(buffer, read, size - read);

                Rrd4Qt.rrdReply("hello, you send me: " + new String(buffer, 0, size));
            }
        }
        catch (Exception|Error e)
        {
            System.err.println(e);
            System.exit(1);
        }
        System.exit(0);
    }

    public static synchronized void rrdReply(String reply)
    {
        try {
            ByteBuffer b = ByteBuffer.allocate(4);
            b.putInt(reply.length());

            Rrd4Qt.outputStream.write(new String(b.array()) , 0, 4);
            Rrd4Qt.outputStream.write(reply, 0, reply.length());
            Rrd4Qt.outputStream.flush();
        }
        catch (Exception e)
        {
            System.err.println(e.toString());
        }
    }

    private static void startWorker(String arg)
    {
        Rrd4QtRunnable worker = new Rrd4QtRunnable(arg);
        Rrd4Qt.threadPool.execute(worker);
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
        Rrd4QtRunnable failRunner = (Rrd4QtRunnable) r;
        String queryId = failRunner.getQueryId();
        Rrd4Qt.rrdReply(queryId + "|ERROR|Max thread queue reached");
    }
}
