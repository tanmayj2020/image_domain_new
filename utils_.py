import numpy as np
import random
from bresenham import bresenham


def mydrawPNG(vector_image):
    initX, initY = int(vector_image[0, 0]), int(vector_image[0, 1])
    final_list = []
    for i in range( 0, len(vector_image)):
        if i > 0:
            if vector_image[i - 1, 2] == 1:
                initX, initY = int(vector_image[i, 0]), int(vector_image[i, 1])

        cordList = list(bresenham(initX, initY, int(vector_image[i, 0]), int(vector_image[i, 1])))
        final_list.extend([list(j) for j in cordList])
        initX, initY = int(vector_image[i, 0]), int(vector_image[i, 1])
    return final_list

def preprocess(sketch_points, side=800):
    sketch_points = sketch_points.astype(np.float)
    sketch_points[:, :2] = sketch_points[:, :2] / np.array([side, side])
    sketch_points[:, :2] = sketch_points[:, :2] * side
    sketch_points = np.round(sketch_points)
    return sketch_points



def strategy3(p1):
    p1 = preprocess(p1 , 800)
    
    p1 = mydrawPNG(p1)
    

    random.shuffle(p1)
    point_1_list = p1[:200]

   

    return point_1_list 
