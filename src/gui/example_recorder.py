'''
Created on Jun 29, 2011

@author: kjellw
'''

from javax.swing import JFrame, JTextField, JFileChooser, JOptionPane
from javax.swing import BoxLayout
from javax.swing import JButton
from javax.swing import JLabel
from javax.swing import JPanel
from javax.swing import BorderFactory
from java.awt import BorderLayout, Dimension
from java.awt import FlowLayout
from gui.paint_area import PaintArea
from api.image_example_dir import ImageExampleDir
from java.lang import Runnable
import java

class ExampleRecorder(JFrame):
    '''
    A GUI for recording examples
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.image_example_dir = None
        #Set up window
        self.setTitle("Example Recorder")
        self.setLocationRelativeTo(None)
        self.setLayout(BoxLayout(self.getContentPane(), BoxLayout.Y_AXIS))
        #Add content to window
        record_file_label_panel = JPanel(FlowLayout())
        record_file_label_panel.add(JLabel("Save to Dir:"))
        self.add(record_file_label_panel)
        file_label_panel = JPanel(FlowLayout())
        self.file_label = JLabel("None Selected")
        file_label_panel.add(self.file_label)
        self.add(file_label_panel)
        #
        change_record_file_panel = JPanel(BorderLayout())
        def change_dir(event):
            chooser = JFileChooser()
            chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
            res = chooser.showDialog(self,"Select")
            if(res==JFileChooser.APPROVE_OPTION):
                selected_file = chooser.getSelectedFile().getCanonicalPath()
                self.file_label.setText(selected_file)
                self.image_example_dir = ImageExampleDir(selected_file)

        change_record_file_panel.add(JButton("Change Dir...", actionPerformed=change_dir), BorderLayout.CENTER)
        self.add(change_record_file_panel)
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
        self.example_paint_area = PaintArea(100,100)
        panel_with_absolute_layout_for_paint_area = JPanel(None)
        panel_with_absolute_layout_for_paint_area.setPreferredSize(Dimension(self.example_paint_area.getWidth(), self.example_paint_area.getHeight()))
        panel_with_absolute_layout_for_paint_area.add(self.example_paint_area)
        panel_with_absolute_layout_for_paint_area.add(self.example_paint_area)
        example_image_panel.add(panel_with_absolute_layout_for_paint_area, BorderLayout.CENTER)
        def change_text(event):
            self.example_paint_area.clear()
        clear_button = JButton("Clear", actionPerformed=change_text)
        example_image_panel.add(clear_button, BorderLayout.SOUTH)
        example_panel.add(example_image_panel)
        save_example_panel = JPanel(BorderLayout())
        def save_example(event):
            if(self.image_example_dir==None):
                JOptionPane.showMessageDialog(self, "No image example dir selected", 
                                              "Could not Save", 
                                              JOptionPane.ERROR_MESSAGE)
            elif(self.example_label_text_field.getText()==None or 
                 self.example_label_text_field.getText()==""):
                JOptionPane.showMessageDialog(self, "No label selected", 
                                              "Could not Save", 
                                              JOptionPane.ERROR_MESSAGE)
            else:
                print("SAVE EXAMPLE")
                label = self.example_label_text_field.getText()
                image_byte_array = self.example_paint_area.image_byte_array()
                self.example_paint_area.clear()
                ied = self.image_example_dir
                class Runner(Runnable):
                    def run(self):
                        ied.save_example(label, image_byte_array)
                #Saving takes to long time to run in GUI thread
                java.lang.Thread(Runner()).start()
        
        save_example_panel.add(JButton("Save >>", actionPerformed=save_example), BorderLayout.CENTER)
        example_panel.add(save_example_panel)
        self.add(example_panel)
        #Show
        self.setSize(Dimension(300,400))
        self.setVisible(True)
        
if __name__ == '__main__':
    ExampleRecorder()