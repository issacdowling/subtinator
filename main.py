#!/usr/bin/env python3
from faster_whisper import WhisperModel
import os
import sys
import argparse
import srt

parser = argparse.ArgumentParser()
parser.add_argument("input_video_path", type=str)
parser.add_argument("--output_dir", type=str, required=False, default=sys.path[0])
parser.add_argument("--stt_model", type=str, required=False, default="medium.en")
parser.add_argument("--stt_path", type=str, required=False, default=f"{sys.path[0]}/stt")
parser.add_argument("-y", type=bool, required=False, default=False, action=argparse.BooleanOptionalAction)
args = parser.parse_args()

srt_path = f"{args.output_dir}/subtitles.srt"
transcript_path = f"{args.output_dir}/transcript.txt"

## Create Whisper model path if it doesn't exist
if not os.path.exists(args.stt_path):
  os.mkdir(args.stt_path)
  print("Created STT Model directory as it didn't exist")

## Let user know about the variables that are in use
print(f"SRT / Transcript output directory set to: {args.output_dir}")
print(f"STT Model size set to: {args.stt_model}")
print(f"STT model path set to: {args.stt_path}")

if args.y == False:
    if os.path.exists(srt_path):
        if input("Existing SRT file found, delete? [Y/n]") == "n":
            exit()
        else:
            os.remove(srt_path)
    if os.path.exists(transcript_path):
        if input("Existing Transcript file found, delete? [Y/n]") == "n":
            exit()
        else:
            os.remove(transcript_path)
else:
    print(f"-y supplied, removing any existing {srt_path} / {transcript_path}")

## Do this so that unfound models are automatically downloaded, but by default we aren't checking remotely at all, and the
## STT directory doesn't need to be deleted just to automatically download other models
try:
  model = WhisperModel(model_size_or_path=args.stt_model, device="cpu", download_root=args.stt_path, local_files_only = True, cpu_threads=6)
except: #huggingface_hub.utils._errors.LocalEntryNotFoundError (but can't do that here since huggingfacehub not directly imported)
  print(f"Downloading Model: {args.stt_model}")
  model = WhisperModel(model_size_or_path=args.stt_model, device="cpu", download_root=args.stt_path, cpu_threads=6)

## Doesn't transcribe the video directly, segments is a generator
segments, info = model.transcribe(args.input_video_path, language="en")

srt_output = ""
plain_output = ""

for line_index, segment in enumerate(segments):
  print(f"{segment.start}s -> {segment.end}s: {segment.text}")
  srt_output += srt.subtitle_from_transcription(line_index + 1, segment.start, segment.end, segment.text)
  plain_output += f"{segment.text}\n"

srt_text = srt_output.strip()

## Save a synced SRT and unsynced TXT
with open(srt_path, "w") as file:
  file.write(srt_text)
print(f"SRT has been saved to {srt_path}")

with open(transcript_path, "w") as file:
  file.write(plain_output)
print(f"Plaintext has been saved to {transcript_path}")
