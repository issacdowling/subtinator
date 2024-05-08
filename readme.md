# Subtitle Generator (SRT), using local Whisper

Creates synced SRT and plaintext output files containing a transcript of the input video.

## Usage

```
./main.py path-to-video [OPTIONS]
```

Run with `--help` for options info

## Environment

### Create Env / Install dependencies
```
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```