package gui;

import javax.swing.*; // frame与widgets
import java.awt.event.*; // 事件
import java.awt.*;


public class simpleGUI2{
	int x = 70;
	int y = 70;
	
	// 先声明所有widgets
	JFrame frame;
	JLabel label;
	JButton button1, button2;
	MyDrawPanel drawPanel;
	
	// 主程序
	public static void main(String[] argv) {
		simpleGUI2 gui = new simpleGUI2();
		gui.go();
	}
	
	// mainFrame运行方法
	public void go() {
		frame = new JFrame();
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		// 画布
		drawPanel = new MyDrawPanel();
				
		// 按钮1
		button1 = new JButton("Change Circle"); // button1省略了this.，下同		
		button1.addActionListener(new ColorButtonListener()); 	
						
		// 按钮2
		button2 = new JButton("Change Label");		
		button2.addActionListener(new LabelButtonListener());
				
		// Label，文本标签
		label = new JLabel("Not clicked");
		
		// 添加widgets到frame
		frame.add(drawPanel, BorderLayout.CENTER);		
		frame.add(button1, BorderLayout.SOUTH);
		frame.add(button2, BorderLayout.EAST);
		frame.add(label, BorderLayout.WEST);
		
		frame.setSize(500, 300);
		frame.setVisible(true);
		
		
	}
	
	// 用inner class实现event listener
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
	
	// inner class实现DrawPanel
	class MyDrawPanel extends JPanel{
		public void paintComponent(Graphics g) {
			// 色块
			// g.setColor(Color.orange);
			// g.fillRect(20, 50, 100, 70);
			
			// 图片
			// Image image = new ImageIcon("C:\\Users\\zhang\\Desktop\\IELTS\\趣图\\A2.png").getImage();
			// g.drawImage(image, 3, 4, this);
			
			// 随机rgb色填充的圆
			// int red = (int) (Math.random() * 256);
			// int green = (int) (Math.random() * 256);
			// int blue = (int) (Math.random() * 256);
			// g.setColor(new Color(red, green, blue));
			// g.fillOval(70, 70, 100, 100);
			
			// 渐变色填充圆。
			// Graphics2D是Graphics子类。frame调用MyDrawPanel时传入参数类型实际上的是Graphics2D。
			// Graphics2D功能更加强大。
			// Graphics2D g2D = (Graphics2D) g;
			// GradientPaint paint = new GradientPaint(70, 70, Color.BLUE, 150, 150, Color.ORANGE); //设定渐变色		
			// g2D.setPaint(paint); // 将色块填入物体
			// g2D.fillOval(70, 70, 100, 100);
			
			// 实现动画效果
			// g.clearRect(0, 0, this.getWidth(), this.getHeight());
			// g.setColor(Color.GREEN);
			// g.fillOval(simpleGUI2.this.x, simpleGUI2.this.y, 40, 40);
		}
	}
	
}
