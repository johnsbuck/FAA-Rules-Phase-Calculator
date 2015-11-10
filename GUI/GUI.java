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

public class GUI {

    private static final boolean TESTING    = false;

    // Constant Fields
    private static final String IDENTIFIER  = "Track ID: ";
    private static final String FRAME_TITLE = "Phase of Flight Calculator";

    // Frame Fields
    private static JFrame frame         = new JFrame(FRAME_TITLE);
    private static JPanel content       = new JPanel(new GridLayout(1, 2));

    // GUI Input Fields
    private static JPanel input         = new JPanel(new GridLayout(3, 1));
    private static JTextField trackID   = new JTextField();
    private static JTextField time      = new JTextField();
    private static JButton analyze      = new JButton("Analyze");

    // GUI Output Fields
    private static JPanel output        = new JPanel(new GridLayout(1, 1));
    private static JTextArea outputText = new JTextArea();

    public static void main(String[] args) {

	createGUI();
	

    }

    /*
     * This section will create and display the User Interface
     *     that will contain the results of the classification
     *     as well as the input fields to select the data to
     *     classify.
     */
    private static void createGUI() {

	// Create the input panel
	if(TESTING)
	    input.setBorder(new LineBorder(Color.GREEN));
	else
	    input.setBorder(new EmptyBorder(10, 10, 10, 10));
	
	JPanel ID = new JPanel(new GridLayout(1, 2));
	ID.add(new JLabel(IDENTIFIER));
	ID.add(trackID);

	JPanel ti = new JPanel(new GridLayout(1, 2));
	ti.add(new JLabel("Time: "));
	ti.add(time);

	// Give the button an action defined elsewhere in this class
	analyze.addActionListener(new ActionListener() {
		public void actionPerformed(ActionEvent e) {
		    buttonAction();
		}
	    });

	input.add(ID);
	input.add(ti);
	input.add(analyze);
	
	// Create the output panel
	if(TESTING)
	    output.setBorder(new LineBorder(Color.RED));
	else
	    output.setBorder(new EmptyBorder(10, 10, 10, 10));
	
	outputText.setEditable(false);
	outputText.setBorder(new BevelBorder(BevelBorder.LOWERED));
	output.add(outputText);

	// Add the input and output panels to the content pane of the frame
	content.add(input);
	content.add(output);
	frame.setContentPane(content);

	// Set properties of the window containing the interface
	frame.setSize(400, 150);
	frame.setResizable(false);
	frame.setVisible(true);
	frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    }

    private static void buttonAction() {
	outputText.setText(trackID.getText() + " " + time.getText());
    }

}