from moviepy.editor import *
import argparse


def make_video(permalink):
    # make a command-line argument parser & add various parameters
    parser = argparse.ArgumentParser(description="Python script to add audio to video clip")
    parser.add_argument("-s", "--start", help="Start duration of the audio file, default is 0", default=0, type=int)
    parser.add_argument("-e", "--end",
                        help="The end duration of the audio file, default is the length of the video file", type=int)
    parser.add_argument("-c", "--composite", help="Whether to add to the existing audio in the video",
                        action="store_true", default=False)
    parser.add_argument("-f", "--volume-factor", type=float, default=1.0)
    # parse the arguments
    args = parser.parse_args()
    start = args.start
    end = args.end
    composite = args.composite
    volume_factor = args.volume_factor
    # print the passed parameters, just for logging
    print(vars(args))

    # load the video
    video_clip = VideoFileClip(f'Download/{permalink}.mp4')
    # load the audio
    audio_clip = AudioFileClip(f'Download/{permalink}.mp3')

    # use the volume factor to increase/decrease volume
    audio_clip = audio_clip.volumex(volume_factor)

    # if end is not set, use video clip's end
    if not end:
        end = video_clip.end
    # make sure audio clip is less than video clip in duration
    # setting the start & end of the audio clip to `start` and `end` paramters
    audio_clip = audio_clip.subclip(start, end)

    # composite with the existing audio in the video if composite parameter is set
    if composite:
        final_audio = CompositeAudioClip([video_clip.audio, audio_clip])
    else:
        final_audio = audio_clip
    # add the final audio to the video
    final_clip = video_clip.set_audio(final_audio)

    # save the final clip
    final_clip.write_videofile(f"FinalVideo/{permalink}.mp4")
    print('\n')


def concatenate_full_video(files):
    i = True
    while i:
        print('You want to concate full video:(Y/N)')
        ans = input()
        if ans == 'Y':
            i = False
            f = []
            for j in files.keys():
                f.append(VideoFileClip(f'FinalVideo/{j}.mp4'))
            print(f)
            full_video = concatenate_videoclips(f)
            full_video.write_videofile(f'FullVideo/{j}.mp4')
        elif ans == 'N':
            i = False
            print('Exit!!!')
        else:
            print("Incorect answer!!!")
