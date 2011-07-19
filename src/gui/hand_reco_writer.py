'''
Created on Jul 19, 2011

@author: kjell
'''
from javax.swing import JFrame, BoxLayout, JPanel, BorderFactory, JTextArea,\
    JButton
from gui.paint_area import PaintArea
from java.awt import BorderLayout
from api.character_classifier import CharacterClassifier

class HandRecoWriter(JFrame):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        #Create classifier
        character_classifier_file = open("../model_creation/character_classifier.dat",'r')
        self.character_classifier = CharacterClassifier(from_string_string=character_classifier_file.read())
        character_classifier_file.close()
        #Set up window
        self.setTitle("HandReco Writer")
        self.setLocationRelativeTo(None)
        self.setLayout(BorderLayout())
        #Input panel
        input_panel = JPanel()
        input_panel.setLayout(BoxLayout(input_panel, BoxLayout.X_AXIS))
        input_panel.setBorder(BorderFactory.createTitledBorder("Input"))
        self.paint_area = PaintArea(100,100)
        input_panel.add(self.paint_area)
        input_options_panel = JPanel()
        input_options_panel.setLayout(BoxLayout(input_options_panel, BoxLayout.Y_AXIS))
        #Write Char
        write_char_panel = JPanel(BorderLayout())
        def write_char(event):
            char = self.character_classifier.classify_image(self.paint_area.image())
            self.text_area.setText(self.text_area.getText() + char)
            self.paint_area.clear()
        write_char_panel.add(JButton("Write Char", actionPerformed=write_char), BorderLayout.NORTH)
        input_options_panel.add(write_char_panel)
        #Space and Correct
        space_and_correct_panel = JPanel(BorderLayout())
        space_and_correct_panel.add(JButton("Space and Correct"), BorderLayout.NORTH)
        input_options_panel.add(space_and_correct_panel)
        #Space
        space_panel = JPanel(BorderLayout())
        def space(event):
            self.text_area.setText(self.text_area.getText() + " ")
        space_panel.add(JButton("Space", actionPerformed=space), BorderLayout.NORTH)
        input_options_panel.add(space_panel)
        #Clear Input Area
        clear_input_area_panel = JPanel(BorderLayout())
        def clear(event):
            self.paint_area.clear()
        clear_input_area_panel.add(JButton("Clear Input Area", actionPerformed=clear), BorderLayout.NORTH)
        input_options_panel.add(clear_input_area_panel)
        input_panel.add(input_options_panel)
        self.add(input_panel, BorderLayout.NORTH)
        text_area_panel = JPanel()
        text_area_panel.setLayout(BorderLayout())
        text_area_panel.setBorder(BorderFactory.createTitledBorder("Text"))
        self.text_area = JTextArea()
        text_area_panel.add(self.text_area, BorderLayout.CENTER)
        self.add(text_area_panel, BorderLayout.CENTER)
        self.pack()
        self.setVisible(True)
        
if __name__ == '__main__':
    HandRecoWriter()