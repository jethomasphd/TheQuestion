# Film production rules

Read docs/FILM_BRIEF.md and docs/editorial_policy.md before changing editorial content.
Never manufacture archival imagery, speech, quotations, source timecodes, licenses, or human approvals.
Use local authorized originals only. Keep unresolved clips as explicit placeholders.
Every final render must invoke the shared release gate. Approval is tied to the exact input manifest.
Do not change approval files to make a build pass. A human must supply publication approval.
Do not commit media, private permission evidence, credentials, or font binaries.
Run `python -m unittest discover -s tests -v` after pipeline changes.
Keep Windows, macOS and Linux support. Invoke subprocesses with argument arrays, never shell=True.
