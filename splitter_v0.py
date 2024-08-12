import os
import moviepy.editor as mp
import logging
import colorlog

# Create a custom logger
logger = logging.getLogger('my_logger')

# Set the log level
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()

# Set the log level for the handler
console_handler.setLevel(logging.DEBUG)

# Create a colored formatter
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
)

# Set the formatter for the console handler
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)

# further_check - if set true, then it will loop again and try to fit more duration in given size limit. this leads to slow processing
def split_video_by_size(video_path, size_limit_mb, further_check = False):

    output_path = 'C:/Users/abhbhagw/Downloads/trim-videos-with-ffmpeg-python-main/'
    # Convert size limit from MB to bytes
    size_limit = size_limit_mb * 1024 * 1024

    print("-------------------------------------------------------------------------------------------------------")
    logger.info("Output Path : " + output_path)
    logger.info("Size limit : " + str(size_limit))
    print("-------------------------------------------------------------------------------------------------------")

    # Load the video
    video = mp.VideoFileClip(video_path)
    video_duration = video.duration
    # Get the file size in bytes
    file_size = os.path.getsize(video_path)
    parts_count = file_size/size_limit
    parts_duration = abs(video_duration/parts_count)

    print("-------------------------------------------------------------------------------------------------------")
    logger.info("Video Duration : " + str(video_duration))
    logger.info("File Size : " + str(file_size))
    logger.info("Predicted Parts Count : " + str(parts_count))
    logger.info("Predicted Parts Duration : " + str(abs(video_duration/parts_count)))
    print("-------------------------------------------------------------------------------------------------------")

    # Initialize variables
    start_time = 0
    end_time = video_duration
    current_part = 1

    # Loop to create video segments
    while start_time < video_duration:
        logger.debug("Start time : " + str(start_time))

        for i in range(1, int(video_duration) + 1, int(parts_duration)):
            logger.debug("loop count : " + str(i))
            # At the end part, make sure it does not exceed the actual video duration 
            if start_time + i > video_duration:
                temp_end_time = video_duration
            else :
                temp_end_time = start_time + i

            logger.debug("start time : " + str(start_time) )
            logger.debug("Temp end time : " + str(temp_end_time))
            # Cut the clip from start_time to temp_end_time
            temp_clip = video.subclip(start_time, temp_end_time)

            # Check if the size is within the limit
            temp_clip_path = output_path + f"temp_part_{current_part}.mp4"
            temp_clip.write_videofile(temp_clip_path, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac', threads = 2)

            # Check if the file size exceeds the limit
            if further_check == True:
                if os.path.getsize(temp_clip_path) > size_limit:
                    logger.debug("Temp clip size : " + str(os.path.getsize(temp_clip_path)) + " Size limit : " + size_limit)
                    os.remove(temp_clip_path)
                    break

            end_time = temp_end_time

            # If file already there with same name, delete it
            if os.path.exists(output_path + f"part_{current_part}.mp4"):
                os.remove(output_path + f"part_{current_part}.mp4")

            os.rename(temp_clip_path, f"part_{current_part}.mp4")

            # if further_check == False:
            #     break
        
        logger.info(f"Part {current_part} saved from {start_time} to {end_time} seconds.")
        start_time = end_time
        current_part += 1

    # Close the video file
    video.close()

# Example usage
video_path = "C:/Users/abhbhagw/Downloads/trim-videos-with-ffmpeg-python-main/ODATA Training - 20 Jul.mp4"
size_limit_mb = 49  # Size limit in MB for each segment
split_video_by_size(video_path, size_limit_mb, True)
