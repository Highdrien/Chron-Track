# FIT as primary import format

**Date:** 2026-05-10
**Status:** active

## Context

Activity data can be exported from Strava/Garmin in three formats: GPX, TCX, and FIT. The app needs to import historical activities from bulk exports and eventually sync new ones.

## Options considered

- **GPX** — Universal XML, but no lap structure or pre-computed summaries. All metrics must be recalculated from trackpoints. 1.7 MB for a half-marathon.
- **TCX** — XML with lap structure and per-point speed/distance. Most verbose at 3.0 MB per half-marathon.
- **FIT** — Binary format from Garmin/ANT+. Compact (396 KB), richest data (session summaries, lap summaries, device info). Well-supported by the `fitparse` Python library.

## Choice

FIT, because it is the most compact (5–8x smaller than XML formats), contains pre-computed session and lap summaries (no need to recalculate from raw trackpoints), and is the native format of Garmin watches and Strava bulk exports.

## Consequences

- Requires the `fitparse` library (pure Python, no compiled dependencies).
- Files are not human-readable; debugging requires tooling.
- The parser architecture (`activity/parser/`) is designed to support additional formats later (GPX, TCX, or API sources) by adding new parser modules that produce the same `ActivityData`/`LapData` dataclasses.
