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


def get_new_end_time(file_size, size_limit_mb, video_duration, counter, part_size):
    if size_limit_mb - (counter * 5) < 0:
        logger.debug("Size will now reduced to less than 0")
        return

    # increase the counter if size differnce is large
    part_size_mb = part_size/(1024*1024)
    if ((part_size_mb - size_limit_mb) / 10 > 2):
        counter += math.floor((part_size_mb - size_limit_mb) / 10)

    size_limit_mb = size_limit_mb - (counter * 5)
    logger.info(f"Temp size limit set to {size_limit_mb} MB")
    parts_count = file_size/(size_limit_mb * 1024 * 1024)
    end_time = abs(video_duration/parts_count)
    return end_time


def split_video_by_size(video_path, fileName, size_limit_mb):

    parts_total_size = 0
    # Convert size limit from MB to bytes
    size_limit = size_limit_mb * 1024 * 1024

    print("-------------------------------------------------------------------------------------------------------")
    logger.info(f"Output Path     : {video_path}")
    logger.info(f"Size limit      : {size_limit_mb} MB")
    logger.info(f"Video File Path : { video_path + fileName }.mp4")
    print("-------------------------------------------------------------------------------------------------------")

    # Load the video
    video = mp.VideoFileClip(video_path + fileName + ".mp4")
    video_duration = video.duration
    # Get the file size in bytes
    file_size = os.path.getsize(video_path + fileName + ".mp4")
    parts_count = file_size/size_limit
    parts_duration = abs(video_duration/parts_count)

    print("-------------------------------------------------------------------------------------------------------")
    logger.info(f"Video Duration          : { video_duration}")
    logger.info(f"File name               : {fileName}")
    logger.info(f"File Size               : { file_size/(1024*1024)} MB")
    logger.info(f"Predicted Parts Count   : { parts_count}")
    logger.info(
        f"Predicted Part Duration : { abs(video_duration/parts_count)}")
    print("-------------------------------------------------------------------------------------------------------")

    # Skip if video is already less than 49 MB video size limit
    if file_size < 49*1024*1024:
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
        else:
            end_time += parts_duration

        logger.debug(f"Current part : { current_part } out of { parts_count }")
        logger.debug(f"Start time   : { start_time }")
        logger.debug(f"End time     : { end_time } out of {video_duration}")

        # Cut the clip from start_time to end_time
        temp_clip = video.subclip(start_time, end_time)

        temp_clip_path = video_path + fileName + \
            f"temp_part_{current_part}.mp4"
        clip_path = video_path + fileName + f"_part_{current_part}.mp4"
        temp_clip.write_videofile(temp_clip_path, codec="libx264",
                                  temp_audiofile='temp-audio.m4a',
                                  remove_temp=True,
                                  audio_codec='aac',
                                  threads=16)

        # If file already there with same name, delete it
        if os.path.exists(clip_path):
            os.remove(clip_path)

        os.rename(temp_clip_path, (fileName + f"_part_{current_part}.mp4"))

        part_size = os.path.getsize(clip_path)
        part_size_mb = part_size/(1024*1024)
        logger.debug(f"Temp clip size : { part_size_mb } MB ")

        pref_counter = 1
        new_end_time = start_time
        # looping until the size of the file is in range of 35 - 50
        while part_size_mb < 35:
            logger.critical(
                f"File {fileName}_part_{current_part}.mp4 size {part_size_mb} MB")
            logger.warning(
                f"Trying to create another performance file : count { pref_counter }")

            # percentage of how much low it is
            percentage = ((50 - part_size_mb)*100)/50
            percentage_inc = math.floor((size_limit_mb * percentage)/100)

            logger.debug(f"Percentage {percentage}, value {percentage_inc}")
            # increase the size limit by that much
            if pref_counter == 1:
                new_size_limit_mb = size_limit_mb + percentage_inc
            else:
                new_size_limit_mb += percentage_inc

            logger.info(f"New Size limit     : {new_size_limit_mb} MB")

            # increase the part duration
            new_part_count = file_size/(new_size_limit_mb*1024*1024)
            new_part_duration = abs(video_duration/new_part_count)

            # At the end part, make sure it does not exceed the actual video duration
            if new_end_time + new_part_duration > video_duration:
                new_end_time = video_duration
            else:
                new_end_time += new_part_duration

            logger.debug(f"New part count    : {new_part_count}")
            logger.debug(f"New part duration : {new_part_duration}")
            logger.debug(f"Start time        : {start_time}")
            logger.debug(f"New end time      : {new_end_time}")
            logger.debug(f"Previous end time : {end_time}")

            # Cut the clip from start_time to end_time
            temp_clip = video.subclip(start_time, new_end_time)

            new_temp_clip_path = video_path + fileName + \
                f"temp_part_{current_part}_{pref_counter}.mp4"

            temp_clip.write_videofile(new_temp_clip_path, codec="libx264",
                                      temp_audiofile='temp-audio.m4a',
                                      remove_temp=True,
                                      audio_codec='aac',
                                      threads=16)

            new_part_size = os.path.getsize(new_temp_clip_path)
            new_part_size_mb = new_part_size/(1024 * 1024)

            # success cond
            if new_part_size_mb < 50 and new_part_size_mb > 35 and new_part_size_mb > part_size_mb:
                # removed the bad clip
                if os.path.exists(clip_path):
                    os.remove(clip_path)
                    logger.critical(
                        f"File deleted because better clip is created with size {new_part_size_mb} MB")

                os.rename(new_temp_clip_path,
                          (fileName + f"_part_{current_part}.mp4"))

                part_size = new_part_size
                part_size_mb = new_part_size_mb
                end_time = new_end_time
                break

            elif new_part_size_mb > 50:
                # removed the new clip
                if os.path.exists(new_temp_clip_path):
                    os.remove(new_temp_clip_path)
                    logger.critical(
                        f"New file deleted because this is worse than previous with size {new_part_size_mb} MB")
                break
            else:
                # if the size is still less than 35 MB
                logger.debug(
                    f"New file is created with size {new_part_size_mb} MB, is still less than 35")
                # removed the bad clip
                if os.path.exists(clip_path):
                    os.remove(clip_path)
                    logger.critical(
                        f"File deleted because better clip is created with size {new_part_size_mb} MB")

                os.rename(new_temp_clip_path,
                          (fileName + f"_part_{current_part}.mp4"))

                part_size = new_part_size
                part_size_mb = new_part_size_mb
                end_time = new_end_time

            pref_counter += 1
            new_end_time = start_time

        # Check if the size is within the limit
        if part_size > 49*1024*1024:
            logger.critical(
                f"File {fileName}_part_{current_part}.mp4 size {part_size/(1024*1024)} MB exceeds size limit 49 MB")
            os.remove(clip_path)
            logger.critical(f"File deleted because it exceeded the limit")

            counter = 1
            temp_end_time = start_time

            while True:
                logger.warning(
                    f"Trying to create another file : count { counter }")
                # Pass the file size
                # Size limit
                # Video Duration
                # Counter - with each counter the size limit will be size by multiple of 5, so the parts_duration will be shorten
                temp_parts_duration = get_new_end_time(
                    file_size, size_limit_mb, video_duration, counter, part_size)

                temp_end_time += temp_parts_duration
                logger.debug(f"Start time        : {start_time}")
                logger.debug(f"New end time      : {temp_end_time}")
                logger.debug(f"Previous end time : {end_time}")

                # Cut the clip from start_time to temp_end_time
                temp_clip = video.subclip(start_time, temp_end_time)

                temp_clip.write_videofile(temp_clip_path,
                                          codec="libx264",
                                          temp_audiofile='temp-audio.m4a',
                                          remove_temp=True,
                                          audio_codec='aac',
                                          threads=16)

                # check new file size
                temp_clip_size = os.path.getsize(temp_clip_path)
                logger.debug(
                    f"Temp clip size : { temp_clip_size/(1024*1024) } MB ")

                # If file already there with same name, delete it
                if os.path.exists(clip_path):
                    os.remove(clip_path)

                os.rename(temp_clip_path, (fileName +
                          f"_part_{current_part}.mp4"))

                if temp_clip_size < 49*1024*1024:
                    logger.warning(
                        f"Created new part video after {counter} try with size { temp_clip_size/(1024*1024) } MB")
                    part_size = temp_clip_size
                    end_time = temp_end_time
                    break
                counter += 1
                temp_end_time = start_time

        parts_total_size += part_size

        logger.info(
            f"Part {current_part} saved from {start_time} to {end_time} seconds.")
        start_time = end_time
        current_part += 1

    logger.warning(
        f"Total size of part file of video { fileName }.mp4 - { parts_total_size/(1024*1024) } MB")
    logger.warning(
        f"Original Video size { fileName }.mp4 - { file_size/(1024*1024) } MB")
    logger.warning(
        f"Size difference { (file_size - parts_total_size)/(1024*1024) } MB")

    # Close the video file
    video.close()


def main(path, size_limit_mb):
    files = getMp4Files(path)

    logger.debug("Count of Mp4 files in path : " + str(len(files)))
    for file in files:
        tempPath = file.split("/")
        fileName = tempPath[-1].split(".mp4")[0]
        logger.debug("Processing File " +
                     str(files.index(file) + 1) + " out of " + str(len(files)))
        split_video_by_size(path, fileName, size_limit_mb)


# Example usage
# video_path = "C:/Users/abhbhagw/Downloads/trim-videos-with-ffmpeg-python-main/"
video_path = os.getcwd().replace("\\", "/")
video_path = video_path + "/"
size_limit_mb = 45  # Size limit in MB for each segment

main(video_path, size_limit_mb)
