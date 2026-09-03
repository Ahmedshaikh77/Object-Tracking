# Contributing

[Project overview](README.md) · [Script guide and known limitations](docs/USAGE.md)

Keep changes focused and describe which of the seven examples they affect. Preserve existing author attribution, source comments, and any third-party notices. Do not add or change licensing as part of an unrelated documentation or behavior update.

## Before proposing a change

- Read the relevant script and its guide together. The current project is a collection of standalone demos, not an import-safe package.
- Discuss dependency/API migrations, camera calibration, new inputs, and tracking behavior as explicit changes. Do not fold them into a documentation-only patch.
- Avoid importing `aruco_markers.py` or `aruco_markers_advanced.py` during tests: both acquire the camera and start processing at import time.
- Keep virtual environments, camera captures (`frame.jpg`), generated videos, and private recordings out of the change. The current repository has no ignore rules for these generated files; inspect `git status` before staging.
- Do not replace the bundled PDFs or sample videos without documenting their provenance, permission to redistribute, and effect on reproduction.

## Safe checks without a camera or GUI

The following syntax check parses every script without importing it, opening a camera, creating a window, or writing Python bytecode. Run it from the repository root:

```bash
python -c "import ast, pathlib; files = sorted(pathlib.Path('src').glob('*.py')); [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in files]; print(f'Parsed {len(files)} scripts')"
git diff --check
git status --short
```

For a documentation-only change, this comparison should print nothing:

```bash
git diff HEAD -- src requirements.txt assets
```

Also check all Markdown links, each example's working directory and filename, and the correspondence between documented prompts and source code. Syntax and link checks do not establish that OpenCV APIs, cameras, codecs, or tracking results work.

## Manual validation for behavior changes

There is no supplied automated runtime suite. When you intentionally change implementation, report the checks you actually ran and what remains untested:

1. Record OS, Python/NumPy/OpenCV versions, and the installed OpenCV distribution. Keep one wheel variant per environment.
2. Use the bundled input first. Record tracker choice, selected region, output mode, exit behavior, and any observed failures; do not publish a favorable frame as an accuracy score.
3. Check both display and file output when affected. Confirm that generated video opens and contains expected frames, not merely that a saved-message was printed.
4. Test cancelled ROI selection, no initial features, loss of all features, unavailable camera, unreadable input, and unsupported codec when those code paths change.
5. Run webcam tests only with permission and a suitable scene. For pose changes, record camera calibration, capture resolution, dictionary, marker ID, measured side length, and units. Dummy calibration is not a measurement reference.

Performance or accuracy claims need a reproducible protocol, annotated ground truth where appropriate, hardware/software details, and reported failures. None is provided by the current repository.

## Useful bug reports

Include the script name, exact command, working directory, terminal choices, traceback or error text, OS and dependency versions, input filename, and whether screen or file mode was used. For camera issues, include index and permission state; for tracking issues, describe the initial region and when tracking failed. Provide only the minimum non-sensitive example needed to reproduce the problem. Do not attach webcam recordings or private data by default.
