import os
import glob
import ffmpeg
from openai import OpenAI

# os.environ["OPENAI_API_KEY"] = ""

client = OpenAI()


def initialize(input_dir):
    """필요 폴더를 생성하고, 디렉터리를 불러와 수행해야 할 파일들을 읽어들입니다."""
    # mp3 파일을 저장하기 위한 폴더 생성
    mp3_folder = os.path.join(input_dir, "mp3")
    if not os.path.exists(mp3_folder):
        os.makedirs(mp3_folder)

    # srt 파일을 저장하기 위한 폴더 생성
    srt_folder = os.path.join(input_dir, "srt")
    if not os.path.exists(srt_folder):
        os.makedirs(srt_folder)

    # mp4 파일 리스트 반환
    inputs = glob.glob(input_dir + "/*.mp4")
    return inputs


def convert_mp4_to_mp3(mp4_file):
    """mp4 파일을 mp3로 변환하여 mp3 폴더에 저장, 반환합니다."""
    # 저장 디렉터리 변경, mp3로 확장자 변경
    output_file = mp4_file.split(".")[0] + ".mp3"
    splitted = output_file.split("/")
    mp3_file = "/".join(splitted[:-1]) + "/mp3/" + splitted[-1]

    # mp3 추출 후 후 저장
    try:
        stream = ffmpeg.input(mp4_file)
        stream = ffmpeg.output(
            stream, mp3_file, acodec="libmp3lame", audio_bitrate="128k"
        )
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        return mp3_file
    except Exception as e:
        raise RuntimeError(f"오디오 추출 중 예기치 못한 오류가 발생했습니다: {str(e)}")


def extract_srt_from_mp3(mp3_file):
    """mp3파일에 대해 srt 자막을 생성합니다."""
    # 저장 디렉터리 변경,  srt로 확장자 변경
    output_file = mp3_file.split(".")[0] + ".srt"
    splitted = output_file.split("/")
    srt_file = "/".join(splitted[:-2]) + "/srt/" + splitted[-1]

    # srt 추출
    audio_file = open(mp3_file, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="srt",
        language="ko",
        prompt="문장을 나눌 때 말이 끊기지 않도록 마침표로 잘 끊어서 생성해주세요.",
        temperature=0,
        # timestamp_granularities=["segment"]    # need response_format="verbose_json"
    )

    # srt 저장
    with open(srt_file, "w", encoding="utf-8") as f:
        f.write(transcription)