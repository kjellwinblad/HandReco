# -*- coding: cp936 -*-

import Image,ImageFilter

Image_filename = "1.bmp"
im = Image.open(Image_filename)
print im.format, im.size, im.mode

width, height = im.size

horizontal_lines = [(0,  i, width, i + 1) for i in range(height)]

candidate_lines = []
ligible_lines = []

for line in horizontal_lines:
    region = im.crop(line)
    if region.histogram()[0] <= 10:
        candidate_lines.append(line)
        
width_two_lines = [line2[1] - line1[1] for line1, line2 in zip(candidate_lines[:-1],  candidate_lines[1:])]

MAX_WIDTH = max(width_two_lines)

previous_line = (0, 0, width, 1)

ligible_lines.append(previous_line)
for line in candidate_lines[1:]:
    if line[1] - previous_line[1] > MAX_WIDTH / 2:
        ligible_lines.append(line)
        previous_line = line

for line in ligible_lines:
    region = region.point(lambda i : 0)
    im.paste(region, line)

im.show()

words_lines = [(0,  line1[1], width, line2[1]) for line1, line2 in zip(ligible_lines[:-1],  ligible_lines[1:])]



