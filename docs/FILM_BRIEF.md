# THE QUESTION THAT REMAINS
## Codex production brief: archival film about encountering Jesus Christ

**Goal:** Build a reproducible 7–9 minute cinematic archival documentary, plus a 90-second trailer and 60-second vertical cut. The intended emotional experience is awe, humility, and an invitation to wrestle with Jesus as historical person, moral teacher, and claimed Christ.

**Central thesis:** Great thinkers, leaders, scientists, artists, and athletes have reached the heights of power, intellect, creativity, or achievement—and still wrestled with questions of truth, suffering, love, death, forgiveness, and ultimate meaning. Some explicitly say they encountered Jesus Christ in answering them.

**Nonnegotiable editorial principle:** Do not falsely suggest all subjects converted, professed orthodox Christian faith, or arrived at the same conclusion. Distinguish testimony, argument, admiration, cultural references, and doubt. The film's force must come from authentic words, not manufactured consensus.

## 1. Assignment to Codex

Build a research-to-release video workflow in this GitHub repository. Verify archival footage and transcripts, document provenance, obtain or flag necessary rights, produce a timecoded paper edit, assemble a placeholder-driven animatic, and render publishable video **only when all assets are verified and cleared and a human explicitly approves release**.

Never invent quotes, timestamps, footage, permissions, or rights. Never fabricate archival audio or impersonate historical figures. Do not circumvent DRM or scrape protected media. Where permissions cannot be established, create a labeled placeholder and an acquisition task.

## 2. Film structure (working timeline)

| Time | Movement | Narrative intent | Candidate voices |
|---|---|---|---|
| 0:00–0:50 | THE QUESTION | Black, silence, faces, laboratories, chambers, stadiums. On-screen questions: What is greatness? What survives death? What is truth? | No attributed invented speech |
| 0:50–2:10 | POWER | Political power and historical fame cannot answer everything; contrast earthly greatness with Jesus' influence | JFK (context only), Reagan, MLK, Bush |
| 2:10–3:20 | KNOWLEDGE | Scientific inquiry and questions beyond empirical measurement | Francis Collins, John Lennox |
| 3:20–4:45 | ART | Fame, suffering, forgiveness, and Jesus' identity | Bono, Jim Carrey, Denzel Washington |
| 4:45–5:50 | VICTORY | Achievement versus ultimate identity | Stephen Curry, Scottie Scheffler, Kaká |
| 5:50–7:25 | THE REVERSAL | MLK's Drum Major Instinct: greatness measured by service, not dominion | MLK, optionally Queen Elizabeth II / Obama |
| 7:25–8:15 | THE INVITATION | Silence and a final open question, not a triumphalist verdict | Authentic final quotation; Mark 8:29 clearly labeled |

Timing is provisional. Preserve context and natural breathing room over strict duration.

**Suggested ending:** Black screen. “Who do you say that I am?” — Mark 8:29 (verify Bible translation and quotation rights). Hold silence. Title: **THE QUESTION REMAINS.** Credits and source ledger.

## 3. Candidate footage and source leads

These URLs are **research leads only**, not verified media, timecodes, or licenses. Codex must locate full originals and verify exact passages before editing.

| ID | Subject | Recording / passage to locate | Function | Starting URL | Risk |
|---|---|---|---|---|---|
| KING_DRUM | Martin Luther King Jr. | *The Drum Major Instinct*, Feb. 4, 1968; Jesus and greatness through service | Thematic spine | https://kinginstitute.stanford.edu/drum-major-instinct | King Estate and recording rights; obtain authorization/review |
| REAGAN_XMAS | Ronald Reagan | Christmas radio address, Dec. 24, 1983; Jesus beyond moral teacher | Christological statement | https://www.reaganlibrary.gov/archives/speech/radio-address-nation-christmas | Confirm recording and its legal status |
| JFK_TREE | John F. Kennedy | National Christmas Tree remarks, Dec. 17, 1962 | Peace and historical setup | https://www.jfklibrary.org/asset-viewer/archives/jfkwha-155-008 | Not direct testimony about Jesus; label context-only |
| BUSH_DEBATE | George W. Bush | 1999 debate response: Christ changed his heart | Personal testimony | https://www.c-span.org/clip/public-affairs-event/user-clip-george-w-bush-on-why-he-admires-christ/4528159 | C-SPAN rights |
| ELIZABETH_XMAS | Elizabeth II | 2011 Christmas broadcast; Jesus and forgiveness | Reconciliation | https://www.royal.uk/christmas-broadcast-2011 | Broadcaster rights |
| OBAMA_EASTER | Barack Obama | Easter Prayer Breakfast, Apr. 7, 2015; Jesus' humility | Ethics and service | https://obamawhitehouse.archives.gov/the-press-office/2015/04/07/remarks-president-and-vice-president-easter-prayer-breakfast | Confirm footage |
| MANDELA_EASTER | Nelson Mandela | Zion Christian Church Easter conference, Apr. 1994 | Resurrection and reconciliation | https://sahistory.org.za/archive/speech-nelson-mandela-zionist-christian-church-easter-conference-moria-3-april-1994 | Transcript lead; matching footage not confirmed |
| COLLINS_TESTIMONY | Francis Collins | BioLogos, *A Testimony* | Science and conversion | https://biologos.org/insights/videos/francis-collins-a-testimony | Producer permission |
| LENNOX_RESURRECTION | John Lennox | *Can a Scientist Believe in the Resurrection?* | Intellectual argument | https://www.youtube.com/watch?v=0jAlsaj16KQ | Verify source and permissions; identify as mathematician |
| BONO_MEANING | Bono | RTÉ interview with Gay Byrne, 2013; Jesus' divinity | Artist and belief | https://www.youtube.com/watch?v=OZnsgvmTJmo | Broadcaster rights; verify full original |
| CARREY_HOMEBOY | Jim Carrey | Homeboy Industries, 2017; Jesus and forgiveness | Suffering and grace | https://www.youtube.com/watch?v=MzyaQ0H5D74 | Context and producer permission |
| DENZEL_BERNARD | Denzel Washington | Conversation with A. R. Bernard, June 2020 | Spiritual transformation | https://www.instagram.com/reel/CB1GzGkDLb3/ | Social excerpt; find full source |
| CURRY_MVP | Stephen Curry | NBA MVP speech, 2015 | Faith amid victory | https://www.youtube.com/watch?v=fvJl02AziO0 | NBA/broadcast rights |
| SCHEFFLER_MASTERS | Scottie Scheffler | Masters press conference, Apr. 9, 2024; identity in Jesus | Faith amid victory | https://asaptext.com/asap_media/media/1079/1207/transcripts/143176.pdf | Transcript is not footage permission |
| KAKA_SECOND | Kaká | I Am Second, *None More Powerful*, 2014 | Belonging to Jesus | https://www.youtube.com/watch?v=LQob6GGbeAk | Producer rights |

Expand with additional verified historical and contemporary voices, including skeptics wrestling sincerely with Jesus. Diversity of perspective is desirable; no tokenism and no manufactured theological agreement.

## 4. Source verification protocol

For **every** proposed clip, capture: speaker, role, event, event date, original producer/broadcaster, original master URL, local authorized asset path, SHA-256, resolution, frame rate, duration, source in/out timecodes, verbatim words, 30 seconds of surrounding context on each side if available, classification, editorial interpretation, rights owner, permission evidence, reviewer, and approval state.

Allowed classifications: `explicit_jesus_testimony`, `christological_argument`, `christian_ethics`, `general_faith`, `critical_questioning`, `context_only`.

Verification states: `unverified`, `source_confirmed`, `transcript_verified`, `context_verified`.

Rights states: `unknown`, `permission_requested`, `cleared`, `public_domain_verified`, `legal_review_required`, `rejected`.

A quotation must not be edited so as to remove meaningful qualifiers, fabricate agreement, conceal a negative, or convert a question into an assertion. A transcript is not evidence that usable video exists. A publicly accessible YouTube video is not a license. Fair use requires case-specific legal review, not an autonomous agent's declaration.

## 5. Visual and sonic direction

**Aesthetic:** museum-grade archival documentary; black, warm ivory, subtle amber; natural archival textures; understated cinematic type; dignified lower thirds with verified name, role, event, and year. Preserve original aspect ratios. Never create fake archival film, lip-sync, or cloned voices.

**Montage:** presidential podiums, church pulpits, laboratories, interview sets, stadium tunnels, empty auditoriums after applause, and hands in service. Only use genuine archival imagery or explicitly non-documentary symbolic footage. Never imply symbolic footage depicts a historical event.

**Sound:** intelligible authentic speech first; gentle restoration; avoid aggressive denoising; instrumental licensed score that rises slowly and drops to silence at decisive moments. Working delivery target -16 LUFS integrated stereo, true peak no greater than -1 dBTP, verified by final listening. Do not use copyrighted commercial recordings without authorization.

**Edit rhythm:** few flashy transitions. Allow pauses. Cut on ideas and human expressions. Contrast fame and humility, intellectual confidence and mystery, applause and silence. Avoid melodramatic narration and political campaign aesthetics.

## 6. Repository layout

```text
README.md
AGENTS.md
docs/
  FILM_BRIEF.md
  editorial_policy.md
  story_outline.md
  paper_edit.md
  source_research.md
  clearance_register.md
  release_checklist.md
data/
  candidates.csv
  sources.json
  clips.json
  rights.json
  timeline.json
  schemas/
assets/
  source/           # gitignored; licensed/authorized originals only
  approved/         # gitignored
  proxy/            # gitignored
  stills/           # licensed only
  music/            # licensed only
scripts/
  validate_sources.py
  probe_media.py
  make_proxies.py
  build_timeline.py
  render.py
  captions.py
  package_release.py
tests/
  test_schema.py
  test_rights_gate.py
  test_timeline.py
  test_captions.py
outputs/
  animatic/
  rough_cut/
  final/
  reports/
requirements.txt
Makefile
.gitignore
```

Do not commit unauthorized or oversized source media, secret credentials, or licensed fonts. Store originals privately and maintain a manifest of checksums.

## 7. Clip metadata example

```json
{
  "clip_id": "KING_DRUM_001",
  "source_id": "KING_DRUM",
  "speaker": "Martin Luther King Jr.",
  "source_url": "https://kinginstitute.stanford.edu/drum-major-instinct",
  "media_path": null,
  "source_sha256": null,
  "source_in_ms": null,
  "source_out_ms": null,
  "verbatim_transcript": null,
  "context_before": null,
  "context_after": null,
  "claim_class": "christian_ethics",
  "narrative_function": "Greatness through service",
  "verification_status": "unverified",
  "rights_status": "unknown",
  "rights_evidence_path": null,
  "publish_approved": false,
  "editorial_notes": "Verify full original audio and contextual meaning."
}
```

Implement JSON Schemas and validation; fail on missing values for approved releases. Never populate unknown timestamps or quotes with guesses.

## 8. Implementation and commands

Use Python 3.11+, FFmpeg/ffprobe, a declarative JSON timeline, pinned dependencies, and repeatable builds. Optional OTIO or FCPXML export for professional finishing. Support macOS and Linux. Implement:

- `make research`: candidate and provenance report; no scraping protected media.
- `make ingest`: accept only locally provided/authorized media; probe and checksum.
- `make verify`: prepare full-context review packets; ASR suggestions require human correction.
- `make proxies`: standardized edit proxies.
- `make animatic`: viewable story with title cards and clearly labeled missing-clip placeholders; **never simulate speech**.
- `make rough`: verified excerpts only; watermark `ROUGH CUT — NOT CLEARED FOR DISTRIBUTION` if any clearance is incomplete.
- `make release-check`: **fail closed** unless every used asset, quotation, still, score, and clip has provenance, rights clearance or documented human legal approval, context review, and explicit human publication approval.
- `make final`: export only after release-check passes.

Required outputs: `master_4k.mp4`, `master_1080p.mp4`, `trailer_90s.mp4`, `vertical_60s.mp4`, `captions_en.srt`, `captions_en.vtt`, `transcript.md`, `sources_and_credits.md`, `edit_decisions.csv`, `rights_report.json`, `build_manifest.json`. If source resolution is low, preserve its actual fidelity inside the 4K canvas; never misrepresent upscaling as genuine 4K.

Test: malformed metadata, clip bounds, sync, caption timings, black frames, audio peaks, reproducible manifests, and—critically—that an uncleared asset blocks final rendering.

## 9. Execution phases and acceptance criteria

### Phase A: Foundation
Create scaffold, README, AGENTS.md, schema, candidate register, sample metadata, Makefile, automated tests. Everything defaults to **unverified and uncleared**. Provide instructions to add local authorized media.

### Phase B: Research dossier
Prioritize MLK, Reagan, Bono, Collins, Carrey, Scheffler. Find original full recordings, identify precise excerpts with timecodes **only if verified**, write context notes, rights owner and permission request. Output `docs/source_research.md`, `docs/paper_edit.md`, and `docs/clearance_register.md`. Do not stop because one source is unavailable; mark blockers and continue.

### Phase C: Animatic
Build a complete watchable 7–9 minute narrative animatic with original title cards, source citations, labeled missing-footage placeholders, legally usable stills or original abstract motion design, and licensed or original music only. If no cleared score exists, use silence rather than unlicensed music. Include pacing and placeholder durations.

### Phase D: Verified rough cut
Replace placeholders with verified and authorized clips; maintain an EDL mapping each final clip to its original source timecode. If missing material, retain placeholders and mark unresolved items. Never call an incomplete rough cut “final.”

### Phase E: Release
Generate final deliverables only when rights, transcript accuracy, contextual integrity, captions, attribution, and human approval all pass. Export credits and source ledger. Provide a one-page editorial report explaining what the film does and does not claim.

**Definition of done:** The repository builds an animatic from scratch with one command; all provenance and rights blockers are visible; tests pass; the edit is reproducible; no false quotations, fake historical footage, or unsupported conversion claims appear; publishable renders cannot bypass the release gate.

## 10. Initial Codex task prompt

> Read `docs/FILM_BRIEF.md` completely. Implement Phase A and as much of Phase B as verifiably possible. Create a functioning, tested Python/FFmpeg repository, metadata schemas, candidate register, rights gate, research dossier, and initial timecoded paper edit. Do not fabricate quotations, timestamps, downloads, or rights. Produce a placeholder animatic if you can do so with permitted original assets. At the end, run tests and report: files created, verified sources, unresolved media/rights, how to preview the animatic, and the exact human actions needed before release. Proceed autonomously on implementation decisions but never autonomously grant publication approval.

## 11. Optional creative treatments

**Version A: The Witnesses.** Maximize authentic testimony and minimal text; subjects speak almost entirely for themselves.

**Version B: The Question.** Include a few sincere doubters and questioners; the dramatic movement is toward Jesus as the unavoidable historical and existential question, not unanimous belief.

**Version C: The Reversal.** Build around MLK's argument that the most consequential life is not the most powerful one. Return to his sermon at the end.

**Default:** Combine B's intellectual honesty with C's emotional culmination. Avoid using public stature as proof of theological truth.

## 12. Human decisions to request before publication

Confirm final title; approve the exact paper edit and interpretations; supply licensed source files or authorize acquisition; resolve all clip/music/still rights; choose scripture translation; approve credits and final cut. The agent should keep building without these decisions but must not publish or claim final clearance.
