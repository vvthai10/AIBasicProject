import matplotlib.pyplot as plt
import pygame,sys,os
import cv2
import shutil
from init import *
'''
Args:
    1. matrix: The matrix read from the input file,
    2. bonus: The array of bonus points,
    3. start, end: The starting and ending points,
    4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
'''
def make_image(matrix, bonus, pickup, portal, start, end, route: list,saveDir = None ):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    route.reverse()
    if(route[len(route)- 1] != start.get_pos()):
        route.append(start.get_pos())
    route.reverse()
    if(route[len(route)- 1] != end.get_pos()):
        route.append(end.get_pos())
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v') #^
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^') #v        
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    #2. Drawing the map
    ax=plt.figure(dpi=100).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=100,color='black')
    if(bonus):
        plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                    marker='P',s=100,color='green')

    if(pickup):
        plt.scatter([i[1] for i in pickup],[-i[0] for i in pickup],
                    marker='D',s=100,color='blue')

    if(portal):
        plt.scatter([i[1] for i in portal],[-i[0] for i in portal],
                    marker='H',s=100,color='pink')
    plt.scatter(start.col,-start.row,marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='silver')

    plt.text(end.col,-end.row,'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.savefig(saveDir + ".png")
    

class Video:
 
    def __init__(self,size):
        # self.path = os.path.dirname(__file__) + "\image"
        self.path = PATH_IMAGES
        # print(self.path)
        self.name = "image"
        self.cnt = 0
 
        # Ensure we have somewhere for the frames
        try:
            os.makedirs(self.path)
        except OSError:
            pass
    
    def make_png(self,screen):
        self.cnt+=1
        fullpath = self.path + self.name + "%08d.png" % self.cnt
        # print(fullpath)
        pygame.image.save(screen,fullpath)
 
    def make_mp4(self, name):
        image_folder = self.path
        video_name = PATH_VIDEO +  name + '.mp4'

        images = [img for img in os.listdir(image_folder) if img.endswith(".png")]

        frame = cv2.imread(os.path.join(image_folder, images[0]))

        height, width, layers = frame.shape

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video = cv2.VideoWriter(video_name, fourcc, FPS, (width,height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))

        cv2.destroyAllWindows()
        video.release()

    def destroy_png(self):
        print("Destroy images")
        self.cnt = 0
        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        print("Finish!!!")

