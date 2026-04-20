# Model Card: VibeFinder 1.0

---

## 1. Model Name

**VibeFinder 1.0**
A content-based music recommender simulation. Given a listener's taste profile, it scores every song in a catalog and returns the top matches with a plain-English explanation for each pick.

---

## 2. Goal / Task

VibeFinder tries to answer one question: *"Which songs in this catalog best match what this listener is looking for right now?"*

It does not predict future behavior or learn from past sessions. It takes a snapshot of stated preferences — genre, mood, energy level, and acoustic taste — and ranks songs against those preferences at that moment. The goal is to surface the most relevant-feeling songs as quickly and transparently as possible.

---

## 3. Data Used

| Property | Value |
|---|---|
| Catalog size | 20 songs |
| Genres covered | 16 (pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, country, r&b, metal, electronic, reggae, k-pop, folk) |
| Moods covered | 10 (happy, chill, intense, moody, focused, relaxed, confident, melancholic, romantic, euphoric) |
| Features per song | 10: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness |
| Source | Fictional catalog hand-crafted for classroom use; no real listening data |

**Limits:** Most genres have only 1–2 songs. The catalog was not sampled from any real demographic so it does not reflect the actual distribution of music tastes across different age groups, cultures, or regions. Numerical features (energy, acousticness, etc.) were assigned by the catalog author, not measured from audio.

---

## 4. Algorithm Summary

For every song in the catalog, VibeFinder adds up points across four checks. The song with the most points is ranked #1.

1. **Genre match (+3 points):** If the song's genre exactly matches what the listener said they like, it earns 3 points — the biggest single reward. Genre is weighted highest because it defines the broadest musical category.

2. **Mood match (+2 points):** If the song's mood label matches the listener's preferred mood, it earns 2 points.

3. **Energy proximity (up to +1.5 points):** The closer the song's energy level is to the listener's target, the more points it earns. A perfect match gives the full 1.5; a song at the opposite end of the scale gives nearly zero. The formula is `1.5 × (1 − difference)`.

4. **Acoustic bonus (+0.5 points):** Only applies if the listener said they enjoy acoustic music and the song scores above 0.6 on acousticness.

Maximum possible score: **7.0 points.** After all songs are scored, they are sorted from highest to lowest and the top 5 are returned. Each result includes the exact points earned per feature so the reasoning is always visible.

---

## 5. Observed Behavior / Biases

**Genre dominates everything (filter bubble risk):** Because genre is worth 3 points, a song from the right genre almost always outranks songs from other genres even when the mood and energy are completely wrong. The clearest example: the `jazz_intensity` profile (wanted intense, high-energy jazz) received "Coffee Shop Stories" — a slow, relaxed jazz track — as its #1 recommendation, ranked above three songs that correctly matched intensity and energy but had the wrong genre label. In a real product this would be a recommendation the user immediately skips and never trusts again.

**Sparse catalog creates forced filter bubbles:** Genres with only one song (classical, r&b, metal, folk, reggae) always produce the same #1 result regardless of what other preferences the listener has. Positions #2–5 then fall back to songs from completely unrelated genres. The `r&b_romantic` profile's top 5 had a gap of 5 points between #1 (6.48) and #2 (1.47) — a sign that the system had nothing meaningful to offer after the first match.

**Mood labels are binary with no synonym awareness:** "Chill" and "relaxed" feel nearly identical to a human but score 0 for each other. A lofi fan who says "relaxed" instead of "chill" misses all three lofi songs in the catalog.

**No interaction memory:** Every session is treated as the listener's first. The system cannot notice that Gym Hero was skipped four times or that Midnight Coding was replayed ten times. Real recommenders weight behavioral signals as their strongest input.

---

## 6. Evaluation Process

Eight user profiles were tested: four standard and four adversarial (designed to expose edge cases).

| Profile | #1 Result | Score | Finding |
|---|---|---|---|
| pop_fan | Sunrise City | 6.47/7.00 | Intuitive — all three main signals aligned |
| chill_studier | Focus Flow | **7.00/7.00** | Perfect score — all four features matched |
| hard_rocker | Storm Runner | 6.48/7.00 | Correct; mood neighbors filled #2 and #3 |
| r&b_romantic | Velvet Signal | 6.48/7.00 | #1 correct; #2–5 scored below 1.5 (catalog sparsity) |
| grief_workout | Iron Curtain | 4.43/7.00 | Genre won; #2 was an acoustic folk song (surprising) |
| classical_student | Nocturne in Blue | 4.96/7.00 | Sparse coverage: only 1 classical song |
| extreme_acoustic | Campfire Letter | 6.76/7.00 | Near-perfect when the genre exists |
| jazz_intensity | Coffee Shop Stories | 3.78/7.00 | **Failure** — wrong mood and energy, ranked #1 by genre alone |

**Weight sensitivity experiment:** For the pop_fan profile, halving the genre weight (3.0 → 1.5) and doubling the energy weight (1.5 → 3.0) moved Gym Hero from #2 to #5, while Rooftop Lights (indie pop, happy) rose to #2. This confirmed that the default weights are genre-centric: a same-genre song with the wrong mood beats cross-genre songs with the right mood.

---

## 7. Intended Use and Non-Intended Use

### Intended use

- **Classroom exploration** of how content-based filtering works.
- **Teaching tool** for understanding trade-offs between scoring features (why genre is weighted more than mood).
- **Demonstration** of filter bubbles and catalog sparsity effects.
- Running experiments by adjusting weights to see how rankings change.

### Not intended for

- Making real music recommendations to real listeners. The catalog is tiny and fictional.
- Any use where recommendation quality affects a user's experience of a real product.
- Drawing conclusions about actual music taste or listener demographics — the dataset has no connection to real listening behavior.
- Replacing collaborative filtering or audio-based similarity systems for production use.

---

## 8. Ideas for Improvement

1. **Mood synonym mapping:** Create a small lookup table that groups semantically similar moods (chill ≈ relaxed, melancholic ≈ sad, confident ≈ intense). Award partial mood credit (e.g., 1.0 instead of 2.0) for a synonym match. This would fix the "chill vs. relaxed" blindness without needing a machine learning model.

2. **Soft genre matching:** Build a genre similarity matrix where adjacent genres earn partial credit — for example, "indie pop" earns 1.5 points (instead of 0) for a "pop" preference, and "metal" earns 1.5 points for a "rock" preference. This would make the `jazz_intensity` failure much less severe since jazz and blues or latin jazz could be partially credited.

3. **Diversity penalty:** Add a rule that deducts 0.5 points when the same artist would appear twice in the top 5. This forces the ranking to surface a wider range of sounds instead of clustering around one artist or sound.

---

## 9. Personal Reflection

**Biggest learning moment:** The `jazz_intensity` failure was the clearest "aha." I expected the system to blend genre, mood, and energy sensibly. Instead, it confidently recommended a mellow coffee-shop song to a listener who asked for intense, high-energy jazz — and it did so because the math was working exactly as designed. That moment made real what "algorithmic bias" means: the system was not broken, it was doing exactly what the weights told it to do. The bias was in the design, not a bug.

**How AI tools helped, and when I double-checked:** AI tools were useful for expanding the song catalog quickly (generating diverse genres and plausible audio feature values) and for structuring the scoring formula. I double-checked the weight values carefully — AI suggestions tend toward round numbers and equal weights, but equal weights would make genre irrelevant compared to the current design where genre is the decisive factor. I had to reason through each weight myself rather than accepting whatever value was proposed first.

**What surprised me about simple algorithms "feeling" like recommendations:** The chill_studier profile achieved a perfect 7.00/7.00 score for "Focus Flow" — and the result genuinely felt correct. That is just four if-statements and one arithmetic formula. There is no neural network, no user history, no audio analysis. The surprising part is not that simple math can work, but that it works just well enough in favorable cases to feel like intelligence, while failing completely in edge cases (jazz_intensity) in a way a human would never fail. Real recommendation apps feel smarter partly because they have millions of songs — sparsity hides the holes.

**What I would try next:** The most impactful next step would be adding behavioral feedback — even a simple "thumbs up / skip" that adjusts weights per session. If a user skips every high-energy song, the energy weight for that session should drop automatically. That single change would turn this from a static profile matcher into something that actually learns, which is the core mechanism behind every modern recommender. After that, I would add the mood synonym table because it would fix the largest category of silent failures at almost no complexity cost.
