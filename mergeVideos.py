import moviepy.editor as mp
import os
import moviepy.editor as mp
import logging
import colorlog
import math

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


def merge_videos_side_by_side(video1_path, video2_path, output_path):
    # Load the video files
    video1 = mp.VideoFileClip(video1_path)
    video2 = mp.VideoFileClip(video2_path)

    # Ensure the videos have the same height
    video2 = video2.resize(height=video1.h)

    # Merge videos side by side
    merged_video = mp.clips_array([[video1, video2]])

    # Write the output video file
    merged_video.write_videofile(output_path, codec="libx264", threads=16)

    # Close the video files
    video1.close()
    video2.close()


# def main(path, size_limit_mb):
#     files = getMp4Files(path)

#     logger.debug("Count of Mp4 files in path : " + str(len(files)))
#     for file in files:
#         tempPath = file.split("/")
#         fileName = tempPath[-1].split(".mp4")[0]
#         logger.debug("Processing File " +
#                      str(files.index(file) + 1) + " out of " + str(len(files)))
#         # split_video_by_size(path, fileName, size_limit_mb)
#         merge_videos_side_by_side(video1_path, video2_path, output_path)


# # Example usage
# # video_path = "C:/Users/abhbhagw/Downloads/trim-videos-with-ffmpeg-python-main/"
# video_path = os.getcwd().replace("\\", "/")
# video_path = video_path + "/"
# size_limit_mb = 45  # Size limit in MB for each segment

# main(video_path, size_limit_mb)

# Example usage
video1_path = "SAP CPI Training, 27 July, 2020_part_1.mp4"
video2_path = "SAP CPI Training, 27 July, 2020_part_2.mp4"
output_path = "C:/Users/abhbhagw/OneDrive - Capgemini/Desktop/Next Courses/SAP CPI (Cloud Platform Integration)/New folder/New folder/merged_video.mp4"

# If file already there with same name, delete it
if os.path.exists(output_path):
    os.remove(output_path)
merge_videos_side_by_side(video1_path, video2_path, output_path)
