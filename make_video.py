import pygame,sys,os
import cv2
import shutil

PATH_IMAGES =  os.path.dirname(__file__) + "\images\\"
PATH_VIDEO = os.path.dirname(__file__) + "\\output\\"
FPS = 15

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
        print("Destroy")
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

