'''
Created on Jun 29, 2011

@author: kjellw
'''

from javax.swing import JComponent
from java.awt import Color , Dimension, RenderingHints
from java.awt.event import MouseMotionListener, MouseListener, InputEvent
import array
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
        #g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, 
        #                   RenderingHints.VALUE_ANTIALIAS_OFF)
        #g.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL,
        #                   RenderingHints.VALUE_STROKE_PURE)
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
            g.drawPolyline(array.array('i', x_list), array.array('i', y_list), len(stroke)) 
            
            
    def clear(self):
        self.strokes = []
        self.current_stroke = []
        self.repaint()
        
    def image(self):
        w = self.getWidth();
        h = self.getHeight();
        non_black_withe_image = BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB)
        self.paint(non_black_withe_image.getGraphics())
        raster=non_black_withe_image.getRaster()
        bi = BufferedImage(w, h, BufferedImage.TYPE_BYTE_BINARY)
        write_raster = bi.getRaster()
        c = array.zeros('i', 4)
        on=wc = array.zeros('i', 1)
        off=array.zeros('i', 1)
        off[0]=1
        for x in range(w):
            for y in range(h):
                c = raster.getPixel(x,y,c)
                if sum(c)!=1020:
                    write_raster.setPixel(x,y, on)
                else:
                    write_raster.setPixel(x,y, off)
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
