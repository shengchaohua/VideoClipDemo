# coding=utf-8

import os
import numpy as np

from pydub import AudioSegment
from ffmpy3 import FFmpeg


def extract_audio_from_video(video, output_audio):
    """
    从视频中提取音频
    :param video: 视频文件
    :param output_audio: 提取到的音频文件
    :return:
    """
    ff = FFmpeg(inputs={video: None}, outputs={output_audio: "-vn -ar 44100 -ac 2 -ab 192 -f wav"})
    ff.run()


def cut_wav(input_dir, wav_name, output_dir, duration=25):
    """
    切割音频，以一定的时间间隔
    :param input_dir: 输入文件夹
    :param wav_name: 输入wav音频文件名
    :param output_dir: 输出文件夹
    :param duration: 时间间隔，单位秒
    :return:
    """
    from math import ceil

    wav_path = os.path.join(input_dir, wav_name)
    audio = AudioSegment.from_mp3(wav_path)

    length = len(audio)
    num_segment = ceil(length / (duration * 1000))

    for i in range(num_segment):
        start_time = i * duration * 1000
        end_time = min(start_time + 25 * 1000, length)
        sliced_audio = audio[start_time:end_time]
        cutted_wav = os.path.join(output_dir, wav_name.split(".")[0] + "-" + str(i) + ".wav")
        sliced_audio.export(cutted_wav, format="wav")


def wav2pcm(wav, pcm):
    """
    wav 转换为 pcm
    :param wav: wav文件
    :param pcm: pcm文件
    :return:
    """
    with open(wav, "rb") as f:
        f.seek(0)
        f.read(44)
        data = np.fromfile(f, dtype=np.int16)
        data.tofile(pcm)


if __name__ == "__main__":
    pwd = os.getcwd()

    input_video_name = "demo.mp4"
    video_dir = os.path.join(pwd, "video")
    video_path = os.path.join(video_dir, input_video_name)

    output_audio_name = "audio.wav"
    output_dir = os.path.join(pwd, "output")
    output_audio_path = os.path.join(output_dir, output_audio_name)

    for file in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, file))

    # 1. 提取音频
    extract_audio_from_video(video_path, output_audio_path)

    # 2. 切割音频
    cut_wav(output_dir, output_audio_name, output_dir)
    os.remove(output_audio_path)

    # 3. 音频格式转换
    audio_files = os.listdir(output_dir)
    for af in audio_files:
        wav_path = os.path.join(output_dir, af)
        pcm_path = wav_path[:-3] + "pcm"
        wav2pcm(wav_path, pcm_path)
