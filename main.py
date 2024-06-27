import os
from tqdm import tqdm
import argparse
from src.func import initialize, convert_mp4_to_mp3, extract_srt_from_mp3


def main():
    parser = argparse.ArgumentParser(description="mp4 파일로 텍스트 추출")
    parser.add_argument(
        "-d",
        "--dir",
        type=str,
        default=os.path.dirname(os.path.abspath(__file__)),
        help="폴더 위치",
    )
    args = parser.parse_args()

    mp4_list = initialize(args.dir)

    for mp4 in tqdm(mp4_list):
        mp3 = convert_mp4_to_mp3(mp4)
        extract_srt_from_mp3(mp3)


if __name__ == "__main__":
    main()
