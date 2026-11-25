Baselines sealed for the 29 time-not-supplied rows that the sweep did not confirm (phantoms, no company date,
or below the $200k turnover floor and never sent to the sweep). Their `session` field is priced_in.py's
default label (bmo), NOT an established session. Moved here, before edge_score.py was re-run, so that
a default label does not read as a 2026-11-25 09:30 ET print: edge_grounded_score.py had refused V2 on it.
The sweep's verdict on each sent name is in ../../sweep.json; the rest are listed in ../../sweep-universe.json `note_v3b`.
