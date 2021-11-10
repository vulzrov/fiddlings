package gui;

import javax.swing.*; // frame��widgets
import java.awt.event.*; // �¼�
import java.awt.*;


public class simpleGUI2{
	int x = 70;
	int y = 70;
	
	// ����������widgets
	JFrame frame;
	JLabel label;
	JButton button1, button2;
	MyDrawPanel drawPanel;
	
	// ������
	public static void main(String[] argv) {
		simpleGUI2 gui = new simpleGUI2();
		gui.go();
	}
	
	// mainFrame���з���
	public void go() {
		frame = new JFrame();
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		// ����
		drawPanel = new MyDrawPanel();
				
		// ��ť1
		button1 = new JButton("Change Circle"); // button1ʡ����this.����ͬ		
		button1.addActionListener(new ColorButtonListener()); 	
						
		// ��ť2
		button2 = new JButton("Change Label");		
		button2.addActionListener(new LabelButtonListener());
				
		// Label���ı���ǩ
		label = new JLabel("Not clicked");
		
		// ���widgets��frame
		frame.add(drawPanel, BorderLayout.CENTER);		
		frame.add(button1, BorderLayout.SOUTH);
		frame.add(button2, BorderLayout.EAST);
		frame.add(label, BorderLayout.WEST);
		
		frame.setSize(500, 300);
		frame.setVisible(true);
		
		
	}
	
	// ��inner classʵ��event listener
	class ColorButtonListener implements ActionListener{
		public void actionPerformed(ActionEvent event) {
			// drawPanel.repaint();
			simpleGUI2.this.x++;
			simpleGUI2.this.y++;
			simpleGUI2.this.drawPanel.repaint();

		}
	}
	
	class LabelButtonListener implements ActionListener{
		public void actionPerformed(ActionEvent event) {
			label.setText("Clicked");
		}
	}
	
	// inner classʵ��DrawPanel
	class MyDrawPanel extends JPanel{
		public void paintComponent(Graphics g) {
			// ɫ��
			// g.setColor(Color.orange);
			// g.fillRect(20, 50, 100, 70);
			
			// ͼƬ
			// Image image = new ImageIcon("C:\\Users\\zhang\\Desktop\\IELTS\\Ȥͼ\\A2.png").getImage();
			// g.drawImage(image, 3, 4, this);
			
			// ���rgbɫ����Բ
			// int red = (int) (Math.random() * 256);
			// int green = (int) (Math.random() * 256);
			// int blue = (int) (Math.random() * 256);
			// g.setColor(new Color(red, green, blue));
			// g.fillOval(70, 70, 100, 100);
			
			// ����ɫ���Բ��
			// Graphics2D��Graphics���ࡣframe����MyDrawPanelʱ�����������ʵ���ϵ���Graphics2D��
			// Graphics2D���ܸ���ǿ��
			// Graphics2D g2D = (Graphics2D) g;
			// GradientPaint paint = new GradientPaint(70, 70, Color.BLUE, 150, 150, Color.ORANGE); //�趨����ɫ		
			// g2D.setPaint(paint); // ��ɫ����������
			// g2D.fillOval(70, 70, 100, 100);
			
			// ʵ�ֶ���Ч��
			// g.clearRect(0, 0, this.getWidth(), this.getHeight());
			// g.setColor(Color.GREEN);
			// g.fillOval(simpleGUI2.this.x, simpleGUI2.this.y, 40, 40);
		}
	}
	
}
