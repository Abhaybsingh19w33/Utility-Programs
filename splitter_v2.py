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

def CheckMp4(file):
    x = file.split(".")
    if x[-1] == "mp4":
        return True
    return False

def getMp4Files(path):
    Mp4Files = []
    files = os.listdir(path)
    for file in files:
        if CheckMp4(file):
            Mp4Files.append(file)
    return Mp4Files

def split_video_by_size(video_path, fileName, size_limit_mb):

    parts_total_size = 0
    # Convert size limit from MB to bytes
    size_limit = size_limit_mb * 1024 * 1024

    print("-------------------------------------------------------------------------------------------------------")
    logger.info("Output Path : " + video_path)
    logger.info("Size limit : " + str(size_limit))
    logger.info("Video File Path : " + video_path + fileName + ".mp4")
    print("-------------------------------------------------------------------------------------------------------")

    # Load the video
    video = mp.VideoFileClip(video_path + fileName + ".mp4")
    video_duration = video.duration
    # Get the file size in bytes
    file_size = os.path.getsize(video_path + fileName + ".mp4")
    parts_count = file_size/size_limit
    parts_duration = abs(video_duration/parts_count)

    print("-------------------------------------------------------------------------------------------------------")
    logger.info("Video Duration : " + str(video_duration))
    logger.info("File name : " + fileName)
    logger.info("File Size : " + str(file_size) + " bytes , in MB " + str(file_size/(1024*1024)))
    logger.info("Predicted Parts Count : " + str(parts_count))
    logger.info("Predicted Single Part Duration : " + str(abs(video_duration/parts_count)))
    print("-------------------------------------------------------------------------------------------------------")

    # Skip if video is already less than video size limit
    if file_size/(1024*1024) < size_limit_mb :
        logger.warning("File is already in limit size")
        video.close()
        return

    # Initialize variables
    start_time = 0
    end_time = 0
    current_part = 1

    # Loop to create video segments
    while start_time < video_duration:

        # At the end part, make sure it does not exceed the actual video duration 
        if end_time + parts_duration > video_duration:
            end_time = video_duration
        else :
            end_time += parts_duration

        logger.debug("Current part : " + str(current_part) + " out of " + str(parts_count))
        logger.debug("Start time : " + str(start_time))
        logger.debug("Temp end time : " + str(end_time))
        # Cut the clip from start_time to end_time
        temp_clip = video.subclip(start_time, end_time)

        # Check if the size is within the limit
        temp_clip_path = video_path + fileName + f"temp_part_{current_part}.mp4"
        temp_clip.write_videofile(temp_clip_path, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac', threads = 1)

        logger.debug("Temp clip size : " + str(os.path.getsize(temp_clip_path)) + " bytes , in MB " + str(os.path.getsize(temp_clip_path)/(1024*1024)))

        # If file already there with same name, delete it
        if os.path.exists(video_path + fileName + f"_part_{current_part}.mp4"):
            os.remove(video_path + fileName + f"_part_{current_part}.mp4")

        os.rename(temp_clip_path, (fileName + f"_part_{current_part}.mp4"))
        
        parts_total_size += os.path.getsize(video_path + fileName + f"_part_{current_part}.mp4")

        logger.info(f"Part {current_part} saved from {start_time} to {end_time} seconds.")
        start_time = end_time
        current_part += 1

    logger.warning("Total size of part file of video " + fileName + ".mp4 - " + str(parts_total_size/(1024*1024)) + " MB")
    
    # Close the video file
    video.close()

def main(path, size_limit_mb):
    files = getMp4Files(path)

    logger.debug("Count of Mp4 files in path : " +  str(len(files)))
    for file in files:
        tempPath = file.split("/")
        fileName = tempPath[-1].split(".mp4")[0]
        split_video_by_size(path, fileName, size_limit_mb)

# Example usage
# video_path = "C:/Users/abhbhagw/Downloads/trim-videos-with-ffmpeg-python-main/"
video_path = os.getcwd().replace("\\","/")
video_path = video_path + "/"
size_limit_mb = 49  # Size limit in MB for each segment

main(video_path, size_limit_mb)