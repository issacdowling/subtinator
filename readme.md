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

#### GPU support
If you want GPU support, remove the `pywhispercpp` that you just downloaded, and build it with Vulkan enabled. Make sure you've got `cmake` and `vulkan-headers` (or your distro's equivalents) installed.

```
git clone --recursive https://github.com/abdeladim-s/pywhispercpp
cd pywhispercpp
git checkout v1.3.0
GGML_VULKAN=1 pip install . # Can be GGML_CUDA if you REALLY want, but Vulkan is cross-platform so why not?
cd ..
```

You DO NOT want to delete this cloned repo, as it contains `libwhisper`, which is needed.
