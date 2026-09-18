# Speaking script — Week 4 seminar, 7 minutes

Runs **6:38** of your 7:00 at **140 words per minute**, a normal presenting rate. Nerves push most people
faster, so the realistic risk is finishing early, not late.

The script deliberately does **not** read the slides. The room can read; the slides carry
the numbers, and you carry the reasoning. Where a slide holds a figure, say what it
*means* rather than reciting it.

**[→]** marks where you advance. **[beat]** is a deliberate pause — do not fill it.

---

## 1 · Can you trust a predicted shape? — 0:00

p53 is the protein that goes wrong in about half of all human tumours. A cancer
researcher has an AI-predicted model of it, and a chemist waiting on her for the exact
positions to aim the first compounds at.

She had already picked them. Off the picture.

**[→]**

## 2 · The helix she almost shipped — 0:20

This is what she picked. A neat helix at positions 18 to 28 — the stretch MDM2 grips to
keep p53 switched off. Genuinely interesting biology. Those side chains were what the
chemist was going to get.

So I asked her what the picture was actually evidence *of*.

**[beat — let them read the quote]**

Floppy in the tube. She already knew that. The clean helix in the model had talked her
out of something she knew about her own protein.

So I measured it, under the same rule she later gave me for the core. That helix averages
68.88 — below the line. Five of its eleven positions fall under it, including two of the
three side chains she had named. The folded core, for comparison, averages 95.29.

The model draws every position with the same confident line. A tidy picture is not a
confident one.

And so the request changed.

**[→]**

## 3 · Which number answers it? — 1:24

Which brings up the thing this module is actually about — choosing the right number
before you look at any result.

AlphaFold marks its own work in two ways. pLDDT is one score per position: is this bit in
the right place? Zero to a hundred, higher is better, below seventy it is telling you not
to rely on it. PAE is one score per *pair* of positions: are these two bits right
relative to each other? That one is a distance, in ångström, so smaller is better.

Her question was about single positions. So pLDDT answers it, and PAE does not.

And the file she pointed me at held only PAE. The per-position scores were inside the
model file, not the one she sent me. I told her.

**[→]**

## 4 · A sharp drop at 293 — 2:20

So: 219 positions, one rule, applied identically to every one of them. Flag anything
below 70.

Twenty-two came back. And this is the shape of it.

**[beat — let them look at the chart]**

High and flat across the whole fold, then it falls off a cliff at position 293. The core
averages 95.29. The last twenty positions average 46.63. And only one percent of the
folded part was flagged at all.

**[→]**

## 5 · The list found her own edge — 2:49

Which is where I had to stop and not simply hand over a list.

Twenty of those twenty-two flags sit in the last twenty positions of her range. Her range
runs about twenty positions past where the protein stops being folded. Those positions
are not faulty. They are floppy — they are supposed to be.

So the shortlist is mostly a map of where she drew the boundary, not of problems inside
the fold.

And the only two hits genuinely inside the fold sit right on the line. Move the cut-off
from 70 to 65 and both of them disappear.

What I refused to do was hand over twenty-two positions as a clean target list.

**[→]**

## 6 · Where the confident fold ends — 3:39

Now — is that tail actually attached to the core, or just floppy at the end of it? That
is a question about relative placement. pLDDT cannot answer it. PAE can. And the PAE
matrix was sitting in the file she sent me the whole time.

Within the core, typical error is 3.6 ångström — the model knows where things sit
relative to each other. From the tail to that core, it is 28.1. The highest number this
file can even express is 31.75.

So it is not that the model places the tail badly. It does not know where it goes.

Two different measures, asked two different questions, both turn at 293. That is the
strongest thing in the analysis, because it is not one threshold restated.

She got her 22 positions, ranked, with the rule printed on the list. But the real finding
is a boundary decision, and it is hers to make: the confident fold ends near 292, not
312.

**[→]**

## 7 · Who did what — 4:49

On AI use. Pi wrote the spec, the script, the results file and the viewer — and found
unprompted that position 183 carries a chemical tag the cell adds later, then correctly
refused to claim that explained the dip. Claude found that the companion file had no
per-position scores at all, and drafted questions for my second interview round.

The part I would point at is verification. Running one script twice proves nothing. So
the screen was rebuilt independently — different parser, different libraries, no shared
code — and returned the same twenty-two positions, the same ranking, the same values. The
file also stores each confidence twice, and both columns agree: 393 of 393.

I ran the interview, chose the questions, set the cut-off and decided what to refuse. The
cut-off was chosen after I had seen the files. Reproducible, but not blind.

**[→]**

## 8 · What this cannot tell you — 5:50

A confidence score only tells you where the model put an atom. Nothing about the chemical
tags the cell adds, nothing about what p53 binds — and this file is a single copy, when
real p53 works as a group of four.

And a high score is not a good target. It says nothing about whether a drug could bind
there. She asked me not to pick targets, and I didn't.

My own gap: I never checked her 94-to-312 range against a source. The whole finding is
about where that range ends.

Next experiment: compare 183 and 185 against a real, measured structure. That is the one
result a cut-off cannot settle.

**[end — 6:38]**

---

## If you are running long

Cut in this order. Each is self-contained; none breaks the thread.

1. **Slide 7**, the Pi/Claude paragraph — keep only the verification paragraph. Saves ~20s.
2. **Slide 3**, the pLDDT/PAE definitions — point at the slide and say "two scores, one per
   position, one per pair; hers is a per-position question." Saves ~20s.
3. **Slide 8**, the first bullet — the limits are on screen and readable. Saves ~15s.

Do **not** cut from slides 2 or 6. They are the near-miss and the placement result, which
are the two things the seminar feedback asked to be added.

## If you are running short

Slide 5 takes expansion best — the "floppy, not faulty" distinction is worth an extra
sentence, and the 70-to-65 sensitivity is worth saying twice.
