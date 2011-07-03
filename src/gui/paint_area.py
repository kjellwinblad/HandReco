'''
Created on Jun 29, 2011

@author: kjellw
'''

from javax.swing import JComponent
from java.awt import Color , Dimension
from java.awt.event import MouseMotionListener, MouseListener, InputEvent
from array import array
from java.awt.image import BufferedImage
from java.io import ByteArrayOutputStream
from javax.imageio import ImageIO

class PaintArea(JComponent):
    '''
    An area where characters etc can be painted.
    '''
    
    #List of strokes to paint
    strokes = []
    current_stroke = []
    
    def update_painting(self, new_strokes, current_stroke):
        if(new_strokes!=[]):
            self.strokes.append(new_strokes)
        self.current_stroke = current_stroke
        self.repaint()
    
    def paint(self, g):
        #Paint background
        g.setColor(self.getBackground())
        g.fillRect(0, 0, self.getWidth(), self.getHeight())
        #Paint foreground
        g.setColor(self.getForeground())
        all_strokes=self.strokes + [self.current_stroke]
        for stroke in all_strokes:
            x_list = []
            y_list = []
            for (x,y) in stroke:
                x_list.append(x)
                y_list.append(y)
            g.drawPolyline(array('i', x_list), array('i', y_list), len(stroke)) 
            
            
    def clear(self):
        self.strokes = []
        self.current_stroke = []
        self.repaint()
        
    def image(self):
        w = self.getWidth();
        h = self.getHeight();
        bi = BufferedImage(w, h, BufferedImage.TYPE_BYTE_BINARY)
        g = bi.createGraphics();
        self.paint(g);
        return bi;
    
    def image_byte_array(self):
        baos = ByteArrayOutputStream();
        ImageIO.write( self.image(), "png", baos );
        baos.flush();
        image_bytes = baos.toByteArray();
        baos.close()
        return image_bytes
    
    
    class MouseHandler(MouseListener, MouseMotionListener):
        
        last_locations_dragged=[]
        
        record_strokes = False
        
        def get_new_strokes_and_clear(self):
            new_strokes = self.last_locations_dragged
            self.last_locations_dragged = []
            return new_strokes
        
        def start_painting(self):
            self.record_strokes = True
            
        def stop_painting(self):
            if(self.record_strokes):
                self.record_strokes = False
                self.repaint_function(self.get_new_strokes_and_clear(), [])
        
        def mouseDragged(self, event):
            if(self.record_strokes):
                self.last_locations_dragged.append((event.getX(), event.getY()))
                self.repaint_function([], self.last_locations_dragged)

        def mouseEntered(self, event):
            if((event.getModifiersEx() & InputEvent.BUTTON1_DOWN_MASK) == InputEvent.BUTTON1_DOWN_MASK):
                self.start_painting()
            
        def mouseExited(self, event):
            self.stop_painting()
            
        def mousePressed(self, event):
            self.start_painting()
        
        def mouseReleased(self, event):
            self.stop_painting()
            
        def __init__(self, repaint_function):
            self.repaint_function = repaint_function
    
    def __init__(self, width=100, height=100):
        '''
        Constructor
        '''
        self.setSize(width, height)
        self.setMaximumSize(Dimension(width, height))
        self.setMinimumSize(Dimension(width, height))
        self.setPreferredSize(Dimension(width, height))
        self.setBackground(Color(1.0,1.0,1.0,1.0))
        self.setForeground(Color(0.0,0.0,0.0,1.0))
        mouse_handler = PaintArea.MouseHandler(self.update_painting)
        self.addMouseMotionListener(mouse_handler)
        self.addMouseListener(mouse_handler)
