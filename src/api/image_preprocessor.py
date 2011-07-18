'''
Created on Jul 18, 2011

@author: kjell
'''
from array import zeros
from array import array
from java.io import File, FileOutputStream
import inspect
import unittest
from api.image_example_dir import ImageExampleDir
from java.awt.image import BufferedImage
from javax.imageio import ImageIO
from sets import Set
import sys

def pixel_has_color(x,y, raster):
    '''Returns true if pixel has black color'''
    get_pixel_parameter = zeros('i', 1)
    pixel = raster.getPixel(x,y,get_pixel_parameter)
    if pixel[0]==0:
        return True
    else:
        return False

def scale_to_fill(buffered_image):
    raster = buffered_image.getData()
    width = raster.getWidth()
    height = raster.getHeight()
    #Get extreem values from the image
    max_x = 0
    min_x = width
    max_y = 0
    min_y = height
    for x in range(0, width):
        for y in range(0,height):
            color = pixel_has_color(x,y, raster)
            if(color):
                if x > max_x:
                    max_x = x
                if x < min_x:
                    min_x = x
                if y > max_y:
                    max_y = y
                if y < min_y:
                    min_y = y
    #Cut out the part of image containing colored pixels
    sub_image = buffered_image.getSubimage(min_x, min_y, max_x-min_x+1,max_y-min_y+1)
    #Scale the image
    resized_image = BufferedImage(width, height, BufferedImage.TYPE_BYTE_BINARY)
    g = resized_image.createGraphics()
    g.drawImage(sub_image, 0, 0, width, height, None)
    g.dispose()
    return resized_image
                    
def divide_into_segments(nr_of_segments, image_buffer):
    width = image_buffer.getWidth()
    height = image_buffer.getHeight()
    segment_width = width / nr_of_segments
    def create_segment(start_pos):
        end = start_pos + segment_width
        if end > width:
            this_segment_with = segment_width - (end-width)
        elif (width - end - segment_width) < 0:
            this_segment_with = width - start_pos
        else:
            this_segment_with = segment_width
        seg = image_buffer.getSubimage(start_pos,0,this_segment_with, height)
        return seg
    segment_starts = range(0,width, segment_width)
    if len(segment_starts) > nr_of_segments:
        del segment_starts[len(segment_starts)-1]
    segments = [create_segment(s) for s in segment_starts]
    return segments

def extract_sorted_component_size_list(image_buffer):
    #Search for unprocessed colored pixels and find the component
    raster = image_buffer.getData()
    width = image_buffer.getWidth()
    height = image_buffer.getHeight()
    #make sure we don't run out of stack space
    old_rec_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(width*height)
    #Remember which pixels have been processed
    processed_colored_pixels = Set()
    def neighbour_pixels(pixel):
        x,y = pixel
        neighbours = [(x-1,y-1),
                      (x-1,y),
                      (x-1,y+1),
                      (x,y-1),
                      (x,y+1),
                      (x+1,y-1),
                      (x+1,y),
                      (x+1,y+1)]
        valid_neighbours = [(x,y) for (x,y) in neighbours 
                            if(x >= 0 and x < width and
                               y >= 0 and y < height)]
        return valid_neighbours
        
    def find_component_length(start_pixel):
        x,y = start_pixel
        if not pixel_has_color(x, y, raster):
            return 0
        elif start_pixel in processed_colored_pixels:
            return 0
        else:
            processed_colored_pixels.add(start_pixel)
            neighbours = neighbour_pixels(start_pixel)
            lengths_of_neighbour_components = [find_component_length(p)
                                              for p in neighbours]
            return 1 + sum(lengths_of_neighbour_components)
    component_lengths = [length for length in 
                         [find_component_length((x,y)) for x in range(width) for y in range(height)]
                         if(length>0)]
    #Set stack limit back to normal    
    sys.setrecursionlimit(old_rec_limit)
    #Component lengths shall be sorted with the largest first
    component_lengths.sort()
    component_lengths.reverse()
    return component_lengths


class TestImagePreprocessor(unittest.TestCase):
    
    def get_example_image(self):
        f = File(str(inspect.getfile( inspect.currentframe() )))
        example_dir = File(File(f.getParentFile().getParentFile().getParentFile(),"character_examples"),"A")
        image_example_dir = ImageExampleDir(example_dir.getCanonicalPath())
        label, image = image_example_dir.__iter__().next()
        return image
    
    def write_image_to_disk(self, image_path, image):
        os = FileOutputStream(image_path)
        ImageIO.write( image, "png", os )
        os.flush()
        os.close()
    
    def test_image_example_dir_iteration(self):
        image = self.get_example_image()
        scaled_image = scale_to_fill(image)
        #Print image to disk to test how it looks like
        self.write_image_to_disk("/tmp/test.png", scaled_image)
    
    def test_divide_into_segments(self):
        orginal_image = self.get_example_image()
        image = scale_to_fill(orginal_image)
        segments = divide_into_segments(7, image)
        i = 0
        for s in segments:
            self.write_image_to_disk("/tmp/segment"+str(i)+".png", s)
            i = i +1
    
    def test_extract_sorted_component_size_list(self):
        orginal_image = self.get_example_image()
        image = scale_to_fill(orginal_image)
        segments = divide_into_segments(7, image)
        for s in segments:
            component_size_list = extract_sorted_component_size_list(s)
            print(component_size_list)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main() 