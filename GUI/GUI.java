import java.awt.*;
import javax.swing.*;
import javax.swing.border.*;

public class GUI {

    private static final boolean TESTING = false;

    private static JFrame frame         = new JFrame();
    private static JPanel content       = new JPanel(new GridLayout(1, 2));
    private static JPanel input         = new JPanel();
    private static JPanel output        = new JPanel(new GridLayout(1, 1));
    private static JTextArea outputText = new JTextArea();

    public static void main(String[] args) {

	createGUI();

    }

    /*
     * This section will create and display the User Interface
     *     that will contain the results of the classification.
     */
    private static void createGUI() {

	// Create the input panel
	if(TESTING)
	    input.setBorder(new LineBorder(Color.GREEN));
	
	// Create the output panel
	output.setBorder(TESTING ? new LineBorder(Color.RED) : new EmptyBorder(10, 10, 10, 10));
	
	outputText.setEditable(false);
	outputText.setBorder(new BevelBorder(BevelBorder.LOWERED));
	output.add(outputText);

	// Add the input and output panels to the content pane of the frame
	content.add(input);
	content.add(output);
	frame.setContentPane(content);

	frame.setSize(400, 200);
	frame.setVisible(true);
	frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    }

}