# videoframe_extraction
Code to extract and transfrom the image frames in a video. The code allows to change the image ratio, resize the images, and extract non-consecutive videoframes among other utils.


<h3> Code parameters in this code </h3>
The code contains several . Here is a list
of the commands and their descriptions.

```

-> --video_path: description=path of the video that we want to use,
            default="video.mp4", type=str

-> --output_directory: description=name of the directory where we want to store the images. The foldel can be non existing,
            default=./extracted_images, type=str

-> --fpsinterval: description=fps interval,
            default=30, type=int

-> --reshaped_width: description='width of the retrieved images',
            default=1920, type=int

-> --reshaped_height: description='height of the retrieved images',
            default=1080, type=int

-> --resize: description='Use the arg to save images in the choosen reshaped size',
            action='store_true'
            
-> --hrotation: description=Use the arg to save images in horizontal position,
            action='store_true'

-> --vrotation: description= Use the arg to save images in vertical position,
            action='store_true'

-> --ratio_modification: description=Use the arg to modify the width to height ratio in the extraacted frames,
            action='store_true'

-> --ratio_width: description=ratio of the width in terms of width to height,
             type=int, default=16

-> --ratio_height: description= ratio of the height in terms of width to height,
            type=int, default=9

-> --rename_videoframe: description= Use the arg to rename the video name for the images,
            action='store_false'

-> --output_file_name= name of the extracted images,
            type=str, default='video'

```
