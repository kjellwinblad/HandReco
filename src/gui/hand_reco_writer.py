'''
Created on Jul 19, 2011

@author: kjell
'''
from javax.swing import JFrame, BoxLayout, JPanel, BorderFactory, JTextArea,\
    JButton, JOptionPane, JScrollPane, JMenuBar, JMenu, JMenuItem, JDialog
from gui.paint_area import PaintArea
from java.awt import BorderLayout, Font, Dimension
from api.character_classifier import CharacterClassifier
from api.word_classifier import WordClassifier
from java.io import File
import inspect

class HandRecoWriter(JFrame):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        #Create classifiers
        #Character classifier
        path_to_this_dir = File(str(inspect.getfile( inspect.currentframe() ))).getParent()
        character_classifier_file = open(File(path_to_this_dir,"character_classifier.dat").getPath(),'r')
        self.character_classifier = CharacterClassifier(from_string_string=character_classifier_file.read())
        character_classifier_file.close()
        #Word classifier
        word_classifier_file = open(File(path_to_this_dir,"word_classifier.dat").getPath(),'r')
        self.word_classifier= WordClassifier(from_string_string=word_classifier_file.read())
        word_classifier_file.close()
        #Set up window
        self.setTitle("HandReco Writer")
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setLocationRelativeTo(None)
        self.setLayout(BorderLayout())
        #Set up menu
        menu_bar = JMenuBar()
        info_menu = JMenu("Info")
        def instructions(event):
            instr = '''
            The program can just recognise capital English characters.
            See Info -> Available Words... for available word corrections.
            
            Good Luck with the writing!'''
            JOptionPane.showMessageDialog(self, instr, 
                          "Instructions", 
                          JOptionPane.INFORMATION_MESSAGE)
        instructions_menu_item = JMenuItem("Instructions...",actionPerformed=instructions)
        info_menu.add(instructions_menu_item)
        def word_corrections(event):
            words_string = ""
            for word in self.word_classifier.words:
                words_string = words_string + word.upper() + "\n"
            text = "The words that can be corrected are:\n\n" +words_string
            dialog = JOptionPane(text, 
                                 JOptionPane.INFORMATION_MESSAGE)
            dialog_wrapper = JDialog(self,"Available Words",False)
            dialog_wrapper.setContentPane(dialog)
            dialog_wrapper.pack()
            dialog_wrapper.setVisible(True)
        word_corrections_menu_item = JMenuItem("Available Words...",actionPerformed=word_corrections)
        info_menu.add(word_corrections_menu_item)
        menu_bar.add(info_menu)
        self.setJMenuBar(menu_bar)
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
        def space_and_correct(event):
            text = self.text_area.getText()
            words = text.split(" ")
            string = words[-1]
            try:
                word = self.word_classifier.classify(string.lower())
                words[-1] = word.upper()
            except:
                JOptionPane.showMessageDialog(self, "Have you entered a character which is not in the alphabet?", 
                              "Could not Correct", 
                              JOptionPane.ERROR_MESSAGE)
                self.text_area.setText(text + " ")
                return
            newText = ""
            for w in words:
                newText = newText + w + " "
            self.text_area.setText(newText)
        space_and_correct_panel.add(JButton("Space and Correct", actionPerformed=space_and_correct), BorderLayout.NORTH)
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
        self.text_area.setLineWrap(True)
        #Increase font size
        font = self.text_area.getFont() 
        self.text_area.setFont(Font(font.getName(), Font.BOLD, 24))
        
        text_area_panel.add(JScrollPane(self.text_area), BorderLayout.CENTER)
        self.add(text_area_panel, BorderLayout.CENTER)
        self.pack()
        self.setSize(Dimension(300,300))
        self.setVisible(True)
        
if __name__ == '__main__':
    HandRecoWriter()