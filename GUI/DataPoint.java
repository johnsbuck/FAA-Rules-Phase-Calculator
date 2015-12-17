/*
 * Container object to hold the three points of data from each row
 *     of the database that we want to send to the clasifier through
 *     a JSON file.
 *
 * @author Nick LaPosta - lapost48
 */

public class DataPoint
{

    private String ts;
    private int alt;
    private int speed;

    public DataPoint(String ts, int alt, int speed)
    {
	this.ts = ts;
	this.alt = alt;
	this.speed = speed;
    }

}