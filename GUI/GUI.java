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

import java.io.*;

public class GUI
{
    // Debug Flag
    private static final boolean TESTING    = false;

    // Constant Fields
    private static final String IDENTIFIER  = "Track ID: ";
    private static final String FRAME_TITLE = "Phase of Flight Calculator";

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
	if(TESTING)
	    inputPanel.setBorder(new LineBorder(Color.GREEN));
	else
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
	if(TESTING)
	    outputPanel.setBorder(new LineBorder(Color.RED));
	else
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

	    // Run python portion of project
	    ProcessBuilder pb = new ProcessBuilder("python", "main.py", "FlightData.txt");
	    Process p = pb.start();
	    BufferedReader pythonOutput = new BufferedReader(new InputStreamReader(p.getInputStream()));

	    // Display python result on output panel
	    outputText.setText(pythonOutput.readLine());
	}
	catch(IOException e)
	{
	    e.printStackTrace();
	}
    }

}