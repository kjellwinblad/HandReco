'''
Created on Jun 29, 2011

@author: kjellw
'''

from javax.swing import JFrame
from javax.swing import BoxLayout
from javax.swing import JButton
from javax.swing import JPanel
from java.awt import BorderLayout
from gui.example_recorder import ExampleRecorder

class MainWindow(JFrame):
    '''
    The main window of the GUI
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        super(MainWindow, self).__init__()

        self.initUI()

    def openExampleRecorder(self,event):
        ExampleRecorder()

    def initUI(self):
        #Set up window
        self.setTitle("HandReco")
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setLocationRelativeTo(None)
        self.setLayout(BoxLayout(self.getContentPane(), BoxLayout.Y_AXIS))
        self.setSize(300,300)
        #Add content to window
        record_examples_panel = JPanel(BorderLayout())
        record_examples_panel.add(JButton("Record Examples", actionPerformed=self.openExampleRecorder), BorderLayout.CENTER)
        self.add(record_examples_panel)
        #
        train_model_panel = JPanel(BorderLayout())
        train_model_panel.add(JButton("Train Model"), BorderLayout.CENTER)
        self.add(train_model_panel)
        #
        classify_examples_panel = JPanel(BorderLayout())
        classify_examples_panel.add(JButton("Classify Examples"), BorderLayout.CENTER)
        self.add(classify_examples_panel)
        #
        classify_character_panel = JPanel(BorderLayout())
        classify_character_panel.add(JButton("Classify Character"), BorderLayout.CENTER)
        self.add(classify_character_panel)
        #Show
        self.setVisible(True)


if __name__ == '__main__':
    MainWindow()
