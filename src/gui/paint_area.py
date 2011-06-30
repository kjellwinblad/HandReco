'''
Created on Jun 29, 2011

@author: kjellw
'''

from javax.swing import JComponent
from java.awt import Color , Dimension
from java.awt.event import MouseMotionAdapter

class PaintArea(JComponent):
    '''
    An area where characters etc can be painted.
    '''
    
    class MouseHandler(MouseMotionAdapter):
       
        def __init__(self):
            print("handle")
       
        def mouseDragged(self, event): 
            print "Mouse dragged"
    
    def __init__(self, width=100, height=100):
        '''
        Constructor
        '''
        self.setSize(width, height)
        self.setMaximumSize(Dimension(width, height))
        self.setMinimumSize(Dimension(width, height))
        self.setPreferredSize(Dimension(width, height))
        self.setBackground(Color(1.0,1.0,1.0,1.0))
        self.addMouseMotionListener(PaintArea.MouseHandler())
   
   

   

        
        