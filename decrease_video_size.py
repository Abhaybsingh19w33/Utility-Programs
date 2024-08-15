import os
import moviepy.editor as mp
import logging
import colorlog
# import math
# import PIL
import pkg_resources
from PIL import Image as pil
from pkg_resources import parse_version
import subprocess

package_version = pkg_resources.get_distribution("pillow").version
print(package_version)
print(parse_version(pil.__version__))
print(parse_version('9.5.0'))

if parse_version(pil.__version__) > parse_version('9.5.0'):
    subprocess.call(['pip', 'uninstall', 'pillow'])
    subprocess.call(['pip', 'install', 'pillow==9.5.0'])
    # Image.ANTIALIAS=Image.LANCZOS

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


def reduce_video_size(input_video_path, output_video_path, target_bitrate="1500k"):
    # Load the video file
    video = mp.VideoFileClip(input_video_path)

    # getting width and height of clip 1
    width = video.w
    height = video.h

    logger.info(f"Video Width { width } Heigh { height }")
    video_resolution = width * height
    logger.info(f"Video resolution {video_resolution}")
    logger.info(f"New Video resolution 1280 * 720 - {1280*720}")
    logger.debug(f"difference old/new { video_resolution/(1280*720) }")
    logger.debug(f"difference old/new { 1/(video_resolution/(1280*720)) }")

    try:
        # Resize the video
        video_resized = video.resize(1/(video_resolution/(1280*720)))

        # Export the resized video with the specified bitrate
        video_resized.write_videofile(
            output_video_path,
            codec="libx264",
            bitrate=target_bitrate,
            audio_codec="aac",
            threads=16,
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )

        # Close the video file
        video_resized.close()

    except Exception as e:
        logger.critical(f"Error : {e}")
        return False

    return True


def main(path, size_limit_mb):
    files = getMp4Files(path)

    logger.debug("Count of Mp4 files in path : " + str(len(files)))
    for file in files:
        tempPath = file.split("/")
        fileName = tempPath[-1].split(".mp4")[0]
        logger.debug("Processing File " +
                     str(files.index(file) + 1) + " out of " + str(len(files)))
        input_video_path = path + fileName + ".mp4"
        output_video_path = path + fileName + "_compressed.mp4"

        file_size = os.path.getsize(input_video_path)
        print("-------------------------------------------------------------------------------------------------------")
        logger.info(
            f"Original file { fileName } size { file_size/(1024*1024) } MB, { file_size/(1024*1024*1024)} GB")
        # Decrease video size with a resolution of 640x360 and a bitrate of 500kbps
        if reduce_video_size(input_video_path, output_video_path):
            compressed_file_size = os.path.getsize(output_video_path)
            logger.info(
                f"Compressed file { fileName }_compressed size { compressed_file_size/(1024*1024) } MB, { compressed_file_size/(1024*1024*1024)} GB")
        print("-------------------------------------------------------------------------------------------------------")


# Example usage
# video_path = "C:/Users/abhbhagw/Downloads/trim-videos-with-ffmpeg-python-main/"
video_path = os.getcwd().replace("\\", "/")
video_path = video_path + "/"
size_limit_mb = 40  # Size limit in MB for each segment

main(video_path, size_limit_mb)
