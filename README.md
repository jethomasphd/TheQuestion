# The Question That Remains

A reproducible archival-documentary workbench and an 8:15 preproduction film, with 90-second and 60-second derivatives. Read [the brief](docs/FILM_BRIEF.md), [research](docs/source_research.md), [paper edit](docs/paper_edit.md) and [editorial report](docs/editorial_report.md).

## Build

Python 3.11+ and FFmpeg/ffprobe on PATH are required. Tested with Python 3.12 and FFmpeg 2025-04-14 build. Install pinned Python dependencies in a virtual environment:

```sh
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# PowerShell: .venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python scripts/render.py animatic
```

On macOS/Linux, `make animatic` is equivalent. Fonts are downloaded from the locked URLs only if absent and checked against recorded SHA-256 values; their OFL license texts are retained. No archival media is downloaded. Set FFMPEG and FFPROBE if the executables are not on PATH. Outputs are under `outputs/animatic/`. `--cut master|trailer|vertical` renders one cut; `--height 360` makes a quick draft.

The full build is silent by design. Captions reproduce on-screen text and placeholder labels; they are not a transcript of unheard archival speech. Trailer and vertical captions are separate. A build manifest records inputs, fonts, toolchain and output checksums. Byte-for-byte movie identity requires the same fonts, pinned Python packages and FFmpeg build.

## Workflows

`make research`, `make verify`, `make proxies`, `make rough`, `make release-check`, `make final`, `make test` map to the scripts in the Makefile. On Windows use their Python commands directly.

Ingest only a file you are authorized to possess; place it inside `assets/source/`, store acquisition evidence privately, then run:

```sh
python scripts/probe_media.py assets/source/master.mp4 --source-id KING_DRUM --authorization docs/private/acquisition.txt
```

Ingest writes a probe/checksum receipt; it deliberately does not set clip verification or publication approval. Transfer measured metadata into the source record, choose timecodes only after reviewing the recording, and complete context/rights evidence. `make verify` generates full-context review requests; nothing is auto-approved. `make rough` uses only context-verified clips with local acquisition evidence, keeping all other slots labeled. Its distribution warning is permanent.

## Release safety

All supplied archival records begin uncleared. `make final` validates all three cuts, every used asset and the human approval hash before rendering. Placeholders, stale hashes, missing evidence, unreviewed context and incomplete captions/listening checks stop the build. The approval record is a human attestation, not an identity-authentication system. The code does not grant approval and never publishes.

Final packaging (once approved) creates `master_4k.mp4`, `master_1080p.mp4`, `trailer_90s.mp4`, `vertical_60s.mp4`, captions, transcript, source credits, EDL, rights report and manifest. Low-resolution originals remain pillarboxed/letterboxed without cropping; a 4K canvas does not make the source native 4K. Licensed music and still compositing are not implemented: the supported edit uses title cards and original source audio. Adding a score requires a new explicit asset/render path and release review.

## Tests and QA

```sh
python -m unittest discover -s tests -v
python scripts/validate_sources.py --release  # must fail for this preproduction edit
python scripts/qa_media.py outputs/animatic/master_1080p.mp4 --duration 495
```

See [release checklist](docs/release_checklist.md) for the exact human actions remaining. Private source media and permission records must never be committed. The font binaries are also excluded from Git; their hashes, download recipe and open licenses are tracked.
