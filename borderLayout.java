package gui;

import javax.swing.*; // frame与widgets
import java.awt.event.*; // 事件
import java.awt.*;

public class borderLayout {
	BorderLayout layout;
	JButton button1;
	JButton button2;
	
	JPanel panel;
	JButton pb1;
	JButton pb2;
	JButton pb3;
	JButton pb4;
	JButton pb5;
	
	JButton button4;
	JButton button5;
	JFrame frame;
	
	public static void main(String[] argv) {
		borderLayout gui = new borderLayout();
		gui.go();
	}
	
	public void go() {
		frame = new JFrame("borderLayout");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		layout = new BorderLayout(20, 10);
		frame.setLayout(layout);
		
		button1 = new JButton("上");
		button2 = new JButton("左");
		
		panel = new JPanel();
		panel.setLayout(new BorderLayout());
		pb1 = new JButton("上");
		pb2 = new JButton("左");
		pb3 = new JButton("中");
		pb4 = new JButton("右");
		pb5 = new JButton("下");
		panel.add(pb1, BorderLayout.NORTH);
		panel.add(pb2, BorderLayout.WEST);
		panel.add(pb3, BorderLayout.CENTER);
		panel.add(pb4, BorderLayout.EAST);
		panel.add(pb5, BorderLayout.SOUTH);
		
		button4 = new JButton("右");
		button5 = new JButton("下");
		
		frame.add(button1, BorderLayout.NORTH);
		frame.add(button2, BorderLayout.WEST);
		frame.add(panel, BorderLayout.CENTER);
		frame.add(button4, BorderLayout.EAST);
		frame.add(button5, BorderLayout.SOUTH);
		
		frame.setSize(500, 500);
		frame.setVisible(true);
	}
}
