# Human release checklist

1. Approve the title, exact paper edit and contextual interpretations, including Fry’s unresolved objection.
2. Supply authorized full masters with acquisition evidence. Run ingest; verify words and source in/out timecodes against the actual recordings, and at least 30 seconds on either side where available.
3. Supply written rights evidence for each used recording, underlying speech, quotation, font, still and score; verify scope covers every cut and distribution channel. Store evidence privately in the repository and record hashes. Legal-review-required is not clearance.
4. Change each approved reservation to `clip`, adjusting durations and downstream edit positions. Keep claims classified accurately. Never invent a source timecode to fill a reservation.
5. Confirm World English Bible Classic and Mark 8:29a’s context. Approve source credits and captions for each of the three cuts.
6. Review a watermarked rough cut, measure and listen to the audio, inspect sync, black frames and safe areas. A sound mix targets -16 LUFS integrated stereo and <= -1 dBTP. Intentional silence has no meaningful integrated loudness target.
7. Complete the per-asset and per-clip human approvals. Run `python scripts/validate_sources.py --fingerprint`; record that input hash in `data/approvals.json`, plus human name/date and a local signed approval record. All checklist entries must be true. Any metadata, code, media or evidence change invalidates the approval.
8. Run release-check, then final. Review the rendered deliverables before publishing. The software does not upload or publish media.

No approval has been granted by this implementation. The preproduction films are not cleared distribution copies.
