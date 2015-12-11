import java.util.ArrayList;

public class QueueList<E> extends ArrayList<E> {

    public QueueList() {
	super();
    }

    public void add(int index, E element) {
	System.out.println("No insertion allowed. Object appended to end.");
	this.add(element);
    }

}