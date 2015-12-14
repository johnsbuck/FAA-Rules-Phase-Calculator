/*
 * GUI for the FAA Phase of Flight Calculator Project
 *
 * This class is to generate the Graphical User Interface
 *     for the project to be used from. This class will also
 *     handle the database querying as well as the execution
 *     of the python module that will do the classification.
 *
 * @author: Nick LaPosta - lapost48
 */

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.border.*;

import java.util.Arrays;
import java.util.ArrayList;

import java.io.*;
import java.sql.*;

public class GUI
{
    // Debug Flag
    private static final boolean TESTING = false;

    // Constant Fields
    private static final String IDENTIFIER      = "Track ID: ";
    private static final String FRAME_TITLE     = "Phase of Flight Calculator";
    private static final String JSON_FILENAME   = "Flight_Data.txt";
    private static final String PYTHON_FILENAME = "main.py";

    // JDBC Connection Fields
    private static final String CONNECTION_URL  = "jdbc:oracle:thin:@//localhost:1521/cablocal";
    private static final String CONNECTION_USER = "uret01";
    private static final String CONNECTION_PASS = "rowan";
    private static final String TABLE_NAME      = "ARTS_RH_CLEANED";
    private static final String ALTITUDE        = "F9_ALTITUDE";
    private static final String SPEED           = "F10_SPEED";
    private static final String TIMESTAMP       = "TO_CHAR(, 'HH24:MI:SS')";

    // Frame Fields
    private static JFrame frame         = new JFrame(FRAME_TITLE);
    private static JPanel contentPanel  = new JPanel(new GridLayout(1, 2));

    // GUI Input Fields
    private static JPanel inputPanel    = new JPanel(new GridLayout(3, 1));
    private static JTextField trackID   = new JTextField();
    private static JTextField time      = new JTextField();
    private static JButton analyze      = new JButton("Analyze");

    // GUI Output Fields
    private static JPanel outputPanel   = new JPanel(new GridLayout(1, 1));
    private static JTextArea outputText = new JTextArea();

    public static void main(String[] args)
    {
	createGUI();
    }

    /*
     * This section will create and display the User Interface
     *     that will contain the results of the classification
     *     as well as the input fields to select the data to
     *     classify.
     */
    private static void createGUI()
    {

	// Create the input panel
	inputPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
	
	// Creates the Panel where the Track ID text field will be placed
	JPanel idPanel = new JPanel(new GridLayout(1, 2));
	idPanel.add(new JLabel(IDENTIFIER));
	idPanel.add(trackID);

	// Creates the Panel where the Time text field will be placed
	JPanel timePanel = new JPanel(new GridLayout(1, 2));
	timePanel.add(new JLabel("Time: "));
	timePanel.add(time);

	// Give the button an action defined elsewhere in this class
	analyze.addActionListener(new ActionListener()
	    {
		public void actionPerformed(ActionEvent e)
		{
		    buttonAction();
		}
	    });

	inputPanel.add(idPanel);
	inputPanel.add(timePanel);
	inputPanel.add(analyze);
	
	// Create the output panel
	outputPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
	
	outputText.setEditable(false);
	outputText.setBorder(new BevelBorder(BevelBorder.LOWERED));
	outputPanel.add(outputText);

	// Add the input and output panels to the content pane of the frame
	contentPanel.add(inputPanel);
	contentPanel.add(outputPanel);
	frame.setContentPane(contentPanel);

	// Set properties of the window containing the interface
	frame.setSize(400, 150);
	frame.setResizable(false);
	frame.setVisible(true);
	frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    }

    private static void buttonAction()
    {
	try
	{
	    Driver jdbcDriver = new oracle.jdbc.driver.OracleDriver();
	    DriverManager.registerDriver(jdbcDriver);
	    Connection con = DriverManager.getConnection(CONNECTION_URL, CONNECTION_USER, CONNECTION_PASS);
	    Statement selectQuery = con.createStatement(ResultSet.TYPE_FORWARD_ONLY, ResultSet.CONCUR_READ_ONLY);
	    ResultSet queryData = selectQuery.executeQuery("SELECT "
							   + ALTITUDE + ","
							   + SPEED + ","
							   + TIMESTAMP + ","
							   + " FROM "
							   + TABLE_NAME);

	    ArrayList<Integer> altitudes = new ArrayList<Integer>();
	    ArrayList<Integer> speed     = new ArrayList<Integer>();
	    ArrayList<String> timestamps = new ArrayList<String>();
	    
	    int[][] cleaningPeriod = new int[2][20];
	    String[] cleaningTimes    = new String[20];
	    for(int i = 0; queryData.next(); i++)
	    {
		cleaningPeriod[0][i % 20] = queryData.getInt(ALTITUDE);
		cleaningPeriod[1][i % 20] = queryData.getInt(SPEED);
		cleaningTimes[i % 20]     = queryData.getString(TIMESTAMP);
		if(i % 20 == 19)
		{
		    // TODO: Finish actual cleaning of data
		    int altitudeMode = getMode(cleaningPeriod[0]);
		    int speedMode    = getMode(cleaningPeriod[1]);
		    
		}
	    }

	    con.close();

	    // TODO: Put values from ArrayLists into a file in proper JSON format
	    

	}
	catch(Exception ex)
	{
	    if(ex instanceof IOException)
	    {
		outputText.setText("IO Issue");
	    }
	    else if(ex instanceof SQLException)
	    {
		outputText.setText("SQL Problems");
	    }
	    else
	    {
		outputText.setText("Other Issues");
	    }
	}

	String result = executePython();
	String[] values = result.split(";");
	String phase = values[0];
	String rules = values[1];
	outputText.setText("Phase of Flight: " + phase + "\nRules of Flight: " + rules);
    }

    private static int getMode(int[] dataPoints)
    {
	Arrays.sort(dataPoints);

	int mode      = -1;
	int prevNum   = -1;
	int count     = 0;
	int prevCount = 0;
	
	for(int num: dataPoints)
	{
	    if(prevNum != num)
	    {
		count = 1;
	    }
	    else
	    {
		count++;
	    }
	    prevNum = num;
	    if(count >= prevCount)
	    {
		prevCount = count;
		mode = prevNum;
	    }
	}
	return mode;
    }

    private static String executePython()
    {
      	try
	{
	    // Run python portion of project
	    ProcessBuilder pb = new ProcessBuilder("python", PYTHON_FILENAME, JSON_FILENAME);
	    Process p = pb.start();	    
	    BufferedReader pythonOutput = new BufferedReader(new InputStreamReader(p.getInputStream()));

	    /* Return the output stream of the called python process
	     *     as a string to be parsed and displayed
	     */
	    return pythonOutput.readLine();
	}
	catch(IOException e)
	{
	    return e.getMessage();
	}
    }
    
}