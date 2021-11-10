package gui;

import javax.swing.*; // frameÓëwidgets
import java.awt.event.*; // ÊÂ¼þ
import java.awt.*;

public class flowLayout {
	JFrame frame;
	FlowLayout layout;
	JButton[] buttons;
	
	public static void main(String[] argv) {
		flowLayout gui = new flowLayout();
		gui.go();
	}
	
	public void go() {
		// layout = new FlowLayout();
		// layout = new FlowLayout(FlowLayout.RIGHT);
		layout = new FlowLayout(FlowLayout.LEFT, 30, 10);
		
		frame = new JFrame("flowLayout");
		buttons = new JButton[9];
		for (int i = 0; i < 9; i++) {
			buttons[i] = new JButton("%d".formatted(i));
			frame.add(buttons[i]);
		}
		
		frame.setLayout(layout);
		frame.setSize(500, 300);
		frame.setVisible(true);
	}
}
