## Credit for this function: https://medium.com/@easylearn.ai/generating-highly-accurate-srt-subtitles-with-ai-openai-whisper-17d25ee3a1a2
## Converts number of seconds to SRT timestamp
def seconds_to_timestamp(seconds: float) -> str:
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    hour = seconds // 3600
    minutes = seconds // 60
    seconds %= 60
    milliseconds = str(int(seconds * 1000 % 1000))[:3]  # Prevent the ocassional super long output
    return "%d:%02d:%02d,%s" % (hour, minutes, seconds, milliseconds)


def subtitle_from_transcription(line_num: int, line_start_seconds: float, line_end_seconds: float, text: str) -> str:
    # This from https://github.com/Arhosseini77/subtitle_whisper/blob/main/module.py (I hadn't yet read up on how SRTs should be formatted, some changes were made)
    return f"{line_num}\n{seconds_to_timestamp(line_start_seconds)} --> {seconds_to_timestamp(line_end_seconds)}\n{text}\n\n"
