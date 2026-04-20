# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0** — a content-based music recommender simulation built for AI110 Module 3.

---

## 2. Intended Use

VibeFinder suggests songs from a small catalog based on a listener's stated genre preference, mood, target energy level, and whether they enjoy acoustic music. It is designed for classroom exploration of how recommender systems work — not for deployment with real users. Every recommendation comes with a plain-English explanation so learners can trace exactly why each song was chosen.

---

## 3. How the Model Works

VibeFinder reads a library of songs, each described by attributes like genre, mood, and energy level. It also reads a "taste profile" that describes what the listener likes. For every song in the library it computes a score by adding up points from four checks:

1. **Genre** — does the song's genre exactly match what the listener prefers? If yes, +3 points (the strongest signal).
2. **Mood** — does the song's mood match? If yes, +2 points.
3. **Energy proximity** — how close is the song's energy to the listener's target? A perfect match adds 1.5 points; a song that is very different adds almost nothing.
4. **Acoustic bonus** — if the listener likes acoustic music and the song scores high on acousticness, +0.5 points.

After every song has a score, they are sorted from highest to lowest and the top five are returned. The math is fully transparent: you can read the score and immediately understand which features drove the result.

---

## 4. Data

The catalog (`data/songs.csv`) contains **20 songs** across **16 genres**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, country, r&b, metal, electronic, reggae, k-pop, and folk. Moods include happy, chill, intense, moody, focused, relaxed, confident, melancholic, romantic, and euphoric. Energy values range from 0.22 (Nocturne in Blue) to 0.97 (Iron Curtain).

The original 10 starter songs were supplemented with 10 additional songs during Phase 2 to improve genre diversity. Despite the expansion, many genres still have only one or two representatives, which limits the variety of recommendations for niche listeners. The catalog was curated to cover a range of fictional artists and styles; it does not reflect any real listening data or demographic.

---

## 5. Strengths

- **Transparent**: every recommendation includes the exact points awarded for each feature, so the reasoning is never hidden.
- **Fast**: the scoring loop runs in under a millisecond even on a 20-song catalog.
- **Accurate for well-represented genres**: profiles that align with the three lofi songs (chill_studier) or the two pop songs (pop_fan) receive intuitive, coherent top-5 results. The chill_studier profile achieved a perfect 7.00/7.00 score for "Focus Flow" because every feature matched exactly.
- **Differentiates clearly**: running the same catalog against four different profiles produces meaningfully different rankings — the hard_rocker and chill_studier share zero songs in their respective top 5.

---

## 6. Limitations and Bias

**Genre lock-in (filter bubble):** Genre carries the highest weight (3.0 out of 7.0 max). For any listener whose preferred genre has only one song in the catalog — like the `classical_student` or `r&b_romantic` profiles — position #1 is always that single song and positions #2–5 fall back to completely unrelated genres. In a real product this would mean a classical listener is perpetually shown the same one track and then a random assortment, creating a narrow filter bubble that reinforces one narrow slice of their taste.

**Mood vocabulary mismatch:** Moods are matched as exact strings. "Relaxed" and "chill" may feel identical to a human listener, but the system scores them as 0 match. A jazz fan who wants a "relaxed" vibe gets no mood credit for chill lofi songs even though they sound nearly identical. This is a structural flaw — the system has no synonym knowledge.

**Conflicting-preference blindness:** The `jazz_intensity` profile reveals a dangerous failure mode: the only jazz song in the catalog ("Coffee Shop Stories", relaxed, energy 0.37) ranks #1 even though it directly contradicts what the user wants (intense, energy 0.85). The genre weight (3.0) overwhelms the mood and energy mismatches combined. A listener following this recommendation would likely hate the result.

**No history, no feedback loop:** The system treats every session identically. It cannot learn that a user skipped "Gym Hero" three times, or that they played "Midnight Coding" on repeat. Real recommenders use this behavioral signal as their most powerful input.

---

## 7. Evaluation

Eight user profiles were tested (four standard, four adversarial):

| Profile | Top Result | Score | Notable Finding |
|---|---|---|---|
| pop_fan | Sunrise City | 6.47 | Intuitive — genre + mood + energy all aligned |
| chill_studier | Focus Flow | 7.00 | Perfect score — all four features matched |
| hard_rocker | Storm Runner | 6.48 | Intuitive; #2 and #3 were correct mood/energy neighbors |
| r&b_romantic | Velvet Signal | 6.48 | #1 correct; #2–5 scored < 1.5 — severe catalog sparsity |
| grief_workout | Iron Curtain | 4.43 | Genre won over mood; #2 was a quiet folk song — surprising |
| classical_student | Nocturne in Blue | 4.96 | Only 1 classical song; catalog gap exposed immediately |
| extreme_acoustic | Campfire Letter | 6.76 | Near-perfect when the genre exists |
| jazz_intensity | Coffee Shop Stories | 3.78 | **Wrong** — the song recommended contradicts the user's energy and mood |

**Weight experiment (pop_fan):** Halving genre weight (3.0→1.5) and doubling energy weight (1.5→3.0) caused Gym Hero to drop from #2 to #5 because its genre advantage was worth less. Rooftop Lights and Neon Heartbeat rose to #2 and #3 because they are energetically closer to the target (0.76 and 0.89 vs 0.80) and their happy mood matched. This confirms that the default genre weight creates a strong bias toward same-genre songs regardless of how mismatched the mood is.

---

## 8. Future Work

- **Synonym mapping for moods:** Build a small lookup table that groups semantically similar moods (chill ≈ relaxed, melancholic ≈ sad) so the system can award partial mood credit rather than binary 0/1.
- **Soft genre matching:** Use a genre similarity matrix so that "indie pop" is partially credited for a "pop" preference, and "metal" is partially credited for a "rock" preference.
- **Diversity bonus:** Add a penalty for recommending the same artist twice in the top 5, so the results surface a wider range of sounds.
- **Behavioral feedback:** Track skips and replays during a session; songs that were skipped should be temporarily down-weighted for that user.
- **Catalog expansion:** At least 5–10 songs per genre are needed before genre filtering becomes meaningful for niche listeners.

---

## 9. Personal Reflection

Building VibeFinder made visible something that is easy to miss when using real apps: a recommender is only as diverse as its data. The jazz_intensity profile was the most revealing experiment — the system confidently recommended a mellow coffee-shop song to someone who wanted intense, high-energy music, simply because it was the only jazz option available. That is exactly how filter bubbles form in production: not because of a bug, but because the system optimizes honestly for the data it has, which is incomplete. Real recommenders on Spotify or YouTube have tens of millions of songs, so genre sparsity is rarely the bottleneck — but the same structural bias operates at scale through collaborative filtering, where users from dominant demographics shape the recommendations that minority-taste users receive. Building a small system first made that mechanism concrete and easy to see.
