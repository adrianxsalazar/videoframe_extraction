# Importing all necessary libraries
import numpy as np
import cv2
import os
import argparse
import ffmpeg
import json


#This code extracts the frames from a video. Additionally, the code allows
#multiple modification on the extracted images such as resizing, rotation, change
#the width/height ratio by cropping the image. The code does not do new things
#but  rather simplies the process of getting frames from a video.


#function to resize images
def image_resizing(image,new_width,new_height):
    """
    @args:
    image: image array
    new_width: new width in the image
    new_height: new height in the image
    """
    #set up the new dimension and resize
    dim=(int(new_width),int(new_height))
    resized_image=cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    #return resized image
    return resized_image

#function to flip images to have an horizontal ratio
def horizontal_rotation_function(image):
    """
    @args:
    image: image array
    """
    #image dimensions
    height, width, color_channel = image.shape

    #Check whether the image is in vertical orientation to rotate it horizontally.
    if height > width:
        image= cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
        return image
    else:
        return image

    return image

#function to flip images to have an vertical ratio
def vertical_rotation_function(image):
    """
    @args:
    image: image array
    """
    #image dimensions
    height, width, color_channel = image.shape

    #Check whether the image is in horizontal orientation to rotate it vertically.
    if width > height:
        image= cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE)
        return image
    else:
        return image

    return image

#function to crop an image to have a specific width/height ratio.
def image_ratio_cropping(image,ratio_width,ratio_height):
    """
    @args:
    image: image array
    ratio_width: proportion of the width e.g. 16
    ratio_height: proportion of the height e.g. 9
    """

    #image dimensions
    height, width, color_channel = image.shape

    #orientation independent cropping
    if width > height:
        longest_side= width
        shortest_side= height
    else:
        longest_side= height
        shortest_side= width


    #get the current width to height ratio.
    current_ratio=float(float(longest_side)/float(shortest_side))

    #Get the desired ratio
    desired_ratio=float(float(ratio_width)/float(ratio_height))

    #In the new image, we need to decrease the "advantage" of the shortest side
    #over the longest side
    if desired_ratio > current_ratio:
        #get the height we need to get
        new_shortest_side=int(float((float(longest_side)*float(ratio_height))/float(ratio_width)))

        #crop the image
        if width > height:
            image=image[0:new_shortest_side,:]
        else:
            image=image[:,0:new_shortest_side]

    #In the new image, we need to reduce the advantage of the longest side over
    #the shortest side
    elif desired_ratio < current_ratio:
        #get the width we need to get.
        new_longest_side=float((float(shortest_side)*float(ratio_width))/float(ratio_height))

        #crop the image
        if width > height:
            image=image[:,0:new_longest_side]
        else:
            image=image[0:new_longest_side:]

    #we have finished with the cropping. Then, return image
    return image

#fucnction to extract images from a video given a framerate extraction
def image_extraction_video(videopath,framerate_extraction_interval,output,
                            resize=False, horizontal_rotation=True,vertical_rotation=False,
                            new_width=1980, new_height=1080, rename_videoframe=False,
                            new_name='initial',ratio_modification=True,
                            ratio_width=16,ratio_height=9):
    """
    @args
    videopath: path of the video where are about to open.
    framerate_extraction_interval: Every how many frames of the video we get an image
    output: path where the ouptput is gonna be saved
    resize (bool): whether the  frames are resized or not.
    horizontal_rtation (bool): Whether rotate the image to have a horizontal orientation.
    vertical_rotation (bool): Whether rotate the image to have a vertical orientation.
    new_width: In case resize == True, this is the new width of the image.
    new_height:In case resize == True, this is the new height of the image.
    """

    #read the video from specified path
    cam = cv2.VideoCapture(videopath)
    video_name=os.path.basename(videopath)
    video_name_no_extension=video_name.split(".")[0]

    #frame counter for filtering frames (currentframe) and for naming (frame_saving_name)
    currentframe = 0
    frame_saving_name=0

    #print statement
    print ('Saving information in %s' % os.path.join(output,str(new_width)+"_"+str(new_height)))

    #create the output folder if it does not exist.
    os.makedirs(os.path.join(output,str(new_width)+"_"+str(new_height)), exist_ok=True)


    #While loop to go through all the frame in the video.
    while(True):

        #reading from frame
        ret,frame = cam.read()

        #if there are frames available, continue.
        if ret:
            # if video is still left continue creating image
            # writing the extracted images
            if currentframe % framerate_extraction_interval == 0:
                #save videos.

                #If rename_videoframe is "True", then, it will rename the frame with

                #the name given in new_name
                if rename_videoframe:
                    image_name = str(new_name)+'_'+str(frame_saving_name)+'.png'
                else:
                    image_name = video_name_no_extension+'_'+str(frame_saving_name)+'.png'


                #Horizontal rotation true will make the width of the image larger than the height.
                if horizontal_rotation:
                    frame=horizontal_rotation_function(frame)

                #Vertical rotation true will make the height of the image larger than the width.
                if vertical_rotation:
                    frame=vertical_rotation_function(frame)

                #perform cropping to get a frame with an specific width/height ratio.
                if ratio_modification:
                    frame=image_ratio_cropping(frame,ratio_width,ratio_height)


                #Rotation and resizing options depending on the given information
                if resize:
                    frame=image_resizing(frame,new_width,new_height)

                #save the frame
                cv2.imwrite(os.path.join(output,str(new_width)+"_"+str(new_height),image_name), frame)
                frame_saving_name+=1

            #increasing counter so that it will,show how many frames are created
            currentframe += 1

        #stop if there are no more frames
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':

    #Parser to make this code work.
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, default='video.mp4', help='path of the video that we want to use')
    parser.add_argument('--output_directory', type=str,
                        default='./extracted_images',
                        help='name of the directory where we want to store the images. The foldel can be non existing')
    parser.add_argument('--fpsinterval', type=int, default=30, help='fps interval')
    parser.add_argument('--reshaped_width', type=int, default=1920,
                        help='width of the retrieved images')
    parser.add_argument('--reshaped_height', type=int, default=1080,
                        help='height of the retrieved images')
    parser.add_argument('--resize', action='store_true', help='Use the arg to save images in the choosen reshaped size')
    parser.add_argument('--hrotation', action='store_true', help='Use the arg to save images in horizontal position')
    parser.add_argument('--vrotation', action='store_true', help='Use the arg to save images in vertical position')
    parser.add_argument('--ratio_modification', action='store_true', help='Use the arg to modify the width to height ratio in the extraacted frames')
    parser.add_argument('--ratio_width', type=int, default=16,
                        help='ratio of the width in terms of width to height')
    parser.add_argument('--ratio_height', type=int, default=9,
                        help='ratio of the height in terms of width to height')
    parser.add_argument('--rename_videoframe', action='store_false',
                        help='Use the arg to rename the video name for the images')
    parser.add_argument('--output_file_name', type=str, default='video',
                        help='name of the extracted images')

    args=parser.parse_args()

    #video_to_frame_folders(args)
    image_extraction_video(args.video_path,args.fpsinterval,args.output_directory,
                                resize=args.resize, horizontal_rotation=args.hrotation,
                                vertical_rotation=args.vrotation,new_width=args.reshaped_width,
                                new_height=args.reshaped_height,rename_videoframe=args.rename_videoframe,
                                new_name=args.output_file_name,ratio_modification=args.ratio_modification,
                                ratio_width=args.ratio_width,ratio_height=args.ratio_height)
