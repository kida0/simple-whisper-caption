[설명]
* 길이가 짧은 영상의 자막을 생성하는 간단한 코드입니다.

[개발 환경]
Python 3.10.12

[실행 방법]
1. 가상환경 실행 후 requirements.txt를 설치합니다.
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
2. .env 파일이나 `src/func.py` 파일에 OPEN_API_KEY를 설정합니다.
3. 영상이 있는 폴더를 `--dir` 또는 `-d`에 지정하여 실행합니다.
```
python3 -d samples
```

[TODO]
- [ ] verbose_json 옵션 추가