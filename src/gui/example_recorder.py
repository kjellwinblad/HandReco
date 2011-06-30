'''
Created on Jun 29, 2011

@author: kjellw
'''

from javax.swing import JFrame, JTextField
from javax.swing import BoxLayout
from javax.swing import JButton
from javax.swing import JLabel
from javax.swing import JPanel
from javax.swing import BorderFactory
from java.awt import BorderLayout
from java.awt import FlowLayout
from gui.paint_area import PaintArea


class ExampleRecorder(JFrame):
    '''
    A GUI for recording examples
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #Set up window
        self.setTitle("Example Recorder")
        self.setLocationRelativeTo(None)
        self.setLayout(BoxLayout(self.getContentPane(), BoxLayout.Y_AXIS))
        #Add content to window
        record_file_label_panel = JPanel(FlowLayout())
        record_file_label_panel.add(JLabel("Save to File:"))
        self.record_file_label = JLabel("None Selected")
        record_file_label_panel.add(self.record_file_label)
        self.add(record_file_label_panel)
        #
        change_record_file_panel = JPanel(BorderLayout())
        change_record_file_panel.add(JButton("Change File..."), BorderLayout.CENTER)
        self.add(change_record_file_panel)
        #
        see_examples_panel = JPanel(BorderLayout())
        see_examples_panel.add(JButton("See Current Examples..."), BorderLayout.CENTER)
        self.add(see_examples_panel)
        #
        example_panel = JPanel()
        example_panel.setLayout(BoxLayout(example_panel, BoxLayout.Y_AXIS))
        example_panel.setBorder(BorderFactory.createTitledBorder("Example:"))
        example_label_panel = JPanel(BorderLayout())
        example_label_panel.setBorder(BorderFactory.createTitledBorder("Example Label:"))
        self.example_label_text_field = JTextField()
        example_label_panel.add(self.example_label_text_field, BorderLayout.CENTER)
        example_panel.add(example_label_panel)
        example_image_panel = JPanel(BorderLayout())
        example_image_panel.setBorder(BorderFactory.createTitledBorder("Example Image:"))
        self.example_paint_area = PaintArea()
        example_image_panel.add(self.example_paint_area, BorderLayout.CENTER)
        example_image_panel.add(JButton("Clear"), BorderLayout.SOUTH)
        example_panel.add(example_image_panel)
        save_example_panel = JPanel(BorderLayout())
        save_example_panel.add(JButton("Save >>"), BorderLayout.CENTER)
        example_panel.add(save_example_panel)
        self.add(example_panel)
        #Show
        self.pack()
        self.setVisible(True)
        
if __name__ == '__main__':
    ExampleRecorder()