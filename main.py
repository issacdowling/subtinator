from faster_whisper import WhisperModel
import os
import sys

help_list = ["-h", "--h", "-help", "--help", "help", "h"]
output_list = ["-o", "-O", "--output", "--output-path"]
model_size_list = ["-m", "-M", "--model", "--model-size"]
download_model_path_list = ["-d", "-D", "--download", "--download-path"]

## Set Video path to first cmdline arg, unless help asked for
try:
  if sys.argv[1] in help_list:
    print("============\nSRT GENERATOR\n============\nUsage:\nmain.py path/to/video [OPTIONS]\n\nVideo file can be any regular video containing audio, it does not need to be pre-converted into just audio\nOptions:\n-o, -O, --output [path]  : Set the path to output files at, will default to the directory containing this script if not specified\n-m, -M, --model [faster-whisper model size] : Set the Whisper model size, will default to large-v3\n-d, -D, --download-path : Set the path to download Whisper models to, will default to a /stt directory in the same directory as this script")
    exit()
  else:
    path_to_video = sys.argv[1]
except IndexError:
  exit("No Video Path Provided. Run with -h for help.")


## Set default variables, then override if specified
output_dir = sys.path[0]
stt_model = "medium.en"
stt_path = f"{sys.path[0]}/stt"


## Set variables based on cmdline args
for index, arg in enumerate(sys.argv):
  if arg in output_list:
    output_dir = sys.argv[index+1]
  if arg in model_size_list:
    stt_model = sys.argv[index+1]
  if arg in download_model_path_list:
    stt_path = sys.argv[index+1]


## Declare variables that rely on the previously set ones
srt_path = f"{output_dir}/subtitles.srt"
transcript_path = f"{output_dir}/transcript.txt"


## Create Whisper model path if it doesn't exist
if not os.path.exists(stt_path):
  os.mkdir(stt_path)
  print("Created STT Model directory as it didn't exist")


## Let user know about the variables that are in use
print(f"SRT / Transcript output directory set to: {output_dir}")
print(f"STT Model size set to: {stt_model}")
print(f"STT model path set to: {stt_path}")


## Credit for this function: https://medium.com/@easylearn.ai/generating-highly-accurate-srt-subtitles-with-ai-openai-whisper-17d25ee3a1a2
## Converts nnumber of seconds to SRT timestamp
def convert(seconds):
  seconds = seconds % (24 * 3600)
  seconds %= 3600
  hour = seconds // 3600
  minutes = seconds // 60
  seconds %= 60
  milliseconds = int(seconds*1000%1000)
  return "%d:%02d:%02d,%d" % (hour, minutes, seconds, milliseconds)


## Delete existing files if wanted
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

## Do this so that unfound models are automatically downloaded, but by default we aren't checking remotely at all, and the
## STT directory doesn't need to be deleted just to automatically download other models
try:
  model = WhisperModel(model_size_or_path=stt_model, device="cpu", download_root=stt_path, local_files_only = True, cpu_threads=6)
except: #huggingface_hub.utils._errors.LocalEntryNotFoundError (but can't do that here since huggingfacehub not directly imported)
  print(f"Downloading Model: {stt_model}")
  model = WhisperModel(model_size_or_path=stt_model, device="cpu", download_root=stt_path, cpu_threads=6)

## Transcribe the video
segments, info = model.transcribe(path_to_video, language='en')

srt_output = ""
plain_output = ""

sub_id = 0
for segment in segments:
  sub_id += 1
  print(f"{segment.start}s -> {segment.end}s: {segment.text}")
  ## This from https://github.com/Arhosseini77/subtitle_whisper/blob/main/module.py
  srt_output += f"{sub_id}\n{convert(segment.start)} --> {convert(segment.end)}\n{segment.text}\n\n"
  plain_output += f"{segment.text}\n"

srt_text = srt_output.strip()

## Save the formatted subtitles to a .srt file
with open(srt_path, 'w') as file:
  file.write(srt_text)
print(f"Subtitles have been saved to {srt_path}")

## Save the unformatted transcript to a .txt file
with open(transcript_path, 'w') as file:
  file.write(plain_output)
print(f"Subtitles have been saved to {transcript_path}")