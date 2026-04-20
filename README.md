# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version implements a **content-based filtering** recommender. It compares a user's stated preferences (genre, mood, and energy level) directly against the attributes of each song in the catalog, computes a weighted score for every song, and returns the top matches. Unlike collaborative filtering — which infers your taste from what *other similar users* have liked — content-based filtering works entirely from the properties of the songs themselves, which makes it transparent and easy to explain but limited to what the song metadata captures.

---

## How The System Works

Real-world music recommenders like Spotify combine two major approaches. **Collaborative filtering** looks at millions of users and finds listeners whose history matches yours, then surfaces what they enjoyed that you haven't heard yet. **Content-based filtering** ignores other users entirely — it analyses the attributes of songs you already like (tempo, mood, energy) and finds new songs with matching properties. Spotify blends both: collaborative signals drive discovery at scale, while content signals ensure recommendations make sense even for new users with no listening history. Our simulation focuses on the content-based side because it is fully explainable — every recommendation can be traced back to a measurable feature.

### Data flow

```mermaid
flowchart TD
    A[data/songs.csv\n20 songs] -->|load_songs| B[List of song dicts]
    U[User Preferences\ngenre · mood · energy · likes_acoustic] --> C
    B --> C{score_song\nfor every song}
    C -->|score + reasons| D[Scored song list]
    D -->|sort descending| E[Ranked list]
    E -->|top k| F[Recommendations\ntitle · score · explanation]
```

### Song features used

Each `Song` stores ten attributes loaded from `data/songs.csv` (20 songs after Phase 2 expansion, covering genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, classical, country, r&b, metal, electronic, reggae, k-pop, folk):

| Feature | Type | Role in scoring |
|---|---|---|
| `genre` | categorical | +3.0 pts for exact match — strongest signal |
| `mood` | categorical | +2.0 pts for exact match |
| `energy` | 0.0–1.0 float | up to +1.5 pts; rewards closeness to user target |
| `acousticness` | 0.0–1.0 float | +0.5 bonus when user prefers acoustic songs |
| `tempo_bpm`, `valence`, `danceability` | numeric | stored but not yet weighted |

### UserProfile attributes

| Attribute | Type | Meaning |
|---|---|---|
| `favorite_genre` | string | e.g. `"hip-hop"` |
| `favorite_mood` | string | e.g. `"focused"` |
| `target_energy` | float | ideal energy level, 0.0–1.0 |
| `likes_acoustic` | bool | unlocks the acousticness bonus |

Four sample profiles are defined in `src/main.py`: `pop_fan`, `chill_studier`, `hard_rocker`, and `r&b_romantic`. Switch the `active_profile_name` variable to compare results.

### Algorithm Recipe (finalized)

```
score = 3.0 × [genre exact match]
      + 2.0 × [mood exact match]
      + 1.5 × (1 − |user_energy − song_energy|)    ← proximity, not magnitude
      + 0.5 × [likes_acoustic AND acousticness > 0.6]

Maximum possible score: 7.0
```

**Why these weights?**
Genre is worth the most (3×) because it defines the broadest musical category — a pop fan almost never wants a metal song regardless of mood. Mood is second (2×) because emotional context is the primary reason most people reach for a particular song. Energy uses a *proximity* formula rather than a raw value so the system rewards songs that are *close* to the user's preference, not just louder or softer. The acoustic bonus is small (0.5×) and optional, giving acoustic-preferring listeners a slight edge without dominating the ranking.

### Known biases and limitations

- **Genre lock-in:** Because genre carries the highest weight (3.0), a listener with a niche genre preference (e.g. `"reggae"`) will almost always see only reggae songs at the top, even if other genres match their mood and energy perfectly. This creates a "filter bubble" that reduces discovery.
- **Mood vocabulary mismatch:** Moods are free-form strings (`"relaxed"`, `"romantic"`, `"euphoric"`). A song labeled `"chill"` and one labeled `"relaxed"` might feel identical to a human listener but score 0 for each other — the system cannot infer synonyms.
- **Sparse representation:** The 20-song catalog has many genres with only 1–2 songs each. A hip-hop fan will always get the same two songs regardless of any other preference signal.
- **No interaction history:** The system treats every session as identical. It cannot learn that a user skipped a song or played another on repeat.

### Ranking rule (whole catalog)

Every song receives a score. The catalog is sorted descending and the top `k` results are returned. Ties break by original catalog order.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Terminal Output

Running `python -m src.main` with each of the four built-in profiles (top 3 shown per profile):

```
Loaded 20 songs from catalog.

────────────────────────────────────────────────────────────
  Profile : pop_fan
  Genre   : pop  |  Mood: happy
  Energy  : 0.8  |  Likes acoustic: False
────────────────────────────────────────────────────────────
  #1  Sunrise City — Neon Echo
      Score : 6.47 / 7.00  |  Why: genre match (+3.0) — pop; mood match (+2.0) — happy; energy very close (+1.47) — song=0.82, target=0.80
  #2  Gym Hero — Max Pulse
      Score : 4.30 / 7.00  |  Why: genre match (+3.0) — pop; energy very close (+1.3) — song=0.93, target=0.80
  #3  Rooftop Lights — Indigo Parade
      Score : 3.44 / 7.00  |  Why: mood match (+2.0) — happy; energy very close (+1.44) — song=0.76, target=0.80

────────────────────────────────────────────────────────────
  Profile : chill_studier
  Genre   : lofi  |  Mood: focused
  Energy  : 0.4  |  Likes acoustic: True
────────────────────────────────────────────────────────────
  #1  Focus Flow — LoRoom
      Score : 7.00 / 7.00  |  Why: genre match (+3.0) — lofi; mood match (+2.0) — focused; energy very close (+1.5) — song=0.40, target=0.40; acoustic match (+0.5) — 0.78
  #2  Midnight Coding — LoRoom
      Score : 4.97 / 7.00  |  Why: genre match (+3.0) — lofi; energy very close (+1.47) — song=0.42, target=0.40; acoustic match (+0.5) — 0.71
  #3  Library Rain — Paper Lanterns
      Score : 4.92 / 7.00  |  Why: genre match (+3.0) — lofi; energy very close (+1.42) — song=0.35, target=0.40; acoustic match (+0.5) — 0.86

────────────────────────────────────────────────────────────
  Profile : hard_rocker
  Genre   : rock  |  Mood: intense
  Energy  : 0.92  |  Likes acoustic: False
────────────────────────────────────────────────────────────
  #1  Storm Runner — Voltline
      Score : 6.48 / 7.00  |  Why: genre match (+3.0) — rock; mood match (+2.0) — intense; energy very close (+1.48) — song=0.91, target=0.92
  #2  Gym Hero — Max Pulse
      Score : 3.48 / 7.00  |  Why: mood match (+2.0) — intense; energy very close (+1.48) — song=0.93, target=0.92
  #3  Iron Curtain — Wrathgate
      Score : 3.43 / 7.00  |  Why: mood match (+2.0) — intense; energy very close (+1.43) — song=0.97, target=0.92

────────────────────────────────────────────────────────────
  Profile : r&b_romantic
  Genre   : r&b  |  Mood: romantic
  Energy  : 0.6  |  Likes acoustic: False
────────────────────────────────────────────────────────────
  #1  Velvet Signal — Demi Shores
      Score : 6.48 / 7.00  |  Why: genre match (+3.0) — r&b; mood match (+2.0) — romantic; energy very close (+1.48) — song=0.61, target=0.60
  #2  Dirt Road Sundown — Honey Spoke
      Score : 1.47 / 7.00  |  Why: energy very close (+1.47) — song=0.58, target=0.60
  #3  Late Night Cipher — Bassline Kings
      Score : 1.46 / 7.00  |  Why: energy very close (+1.46) — song=0.63, target=0.60
```

The `r&b_romantic` profile exposes the **sparse catalog bias** clearly — only one r&b song exists, so positions #2 and #3 are filled by energy-proximity matches with no genre or mood alignment (scores < 1.5). This is the "filter bubble" effect in action: when the catalog lacks songs in the user's preferred genre, the system has nothing meaningful to offer beyond the single exact match.

---

## Experiments You Tried

### Experiment 1 — Weight shift (genre_w 3.0→1.5, energy_w 1.5→3.0)

Run `python -m src.main` and look at the **WEIGHT EXPERIMENT** section at the bottom.

With **default weights** (genre=3.0, energy=1.5), the pop_fan ranking is:
`Sunrise City → Gym Hero → Rooftop Lights → Neon Heartbeat → Dirt Road Sundown`

With **experimental weights** (genre=1.5, energy=3.0), it becomes:
`Sunrise City → Rooftop Lights → Neon Heartbeat → Dirt Road Sundown → Gym Hero`

**Gym Hero drops from #2 to #5.** Why? With default weights, Gym Hero earned 3.0 genre points that offset its mood mismatch. When genre dropped to 1.5, Rooftop Lights and Neon Heartbeat — which both match the "happy" mood and are energetically closer to target — overtook it. Energy proximity now decides the race, rewarding cross-genre songs with the right vibe over same-genre songs with the wrong mood.

### Experiment 2 — Adversarial profiles (edge cases)

Four adversarial profiles were added to `src/main.py` to stress-test the scoring logic:

| Profile | Conflict designed | What happened |
|---|---|---|
| `grief_workout` | metal + melancholic (catalog has no such combo) | Genre won: Iron Curtain (#1) even though it's "intense", then a quiet folk song (#2) — surprising |
| `classical_student` | classical + focused (only 1 classical song) | Filter bubble exposed: #1 correct, #2–5 are random low-energy songs |
| `extreme_acoustic` | folk + melancholic + very low energy | Worked well — the catalog actually has this song |
| `jazz_intensity` | jazz + intense (only jazz song is "relaxed") | System failure: recommended a mellow coffee-shop song to someone who wanted intense high-energy music |

The `jazz_intensity` result is the clearest bias finding: the genre weight of 3.0 alone elevated an energetically wrong song above three songs that correctly matched mood and energy but had the wrong genre label.

---

## Limitations and Risks

- Works only on a 20-song fictional catalog — no real listening data.
- Genre lock-in: a single-genre listener always gets the same #1 after catalog sparsity is hit.
- Mood labels are binary strings with no synonym awareness ("chill" ≠ "relaxed").
- No interaction memory — every session starts from scratch.
- The `jazz_intensity` profile demonstrated a complete failure: the system recommended the opposite of what was asked because genre weight dominated mood and energy mismatches.

Full analysis in [model_card.md](model_card.md).

---

## Reflection

[**→ Full Model Card (VibeFinder 1.0)**](model_card.md)

Building VibeFinder made one thing concrete that is easy to miss when using real apps: a recommender is only as good as the data behind it, and its biases are built into the weights, not hidden in complexity. The `jazz_intensity` experiment was the clearest moment — the system confidently returned the wrong song because the math was working exactly as designed. That is not a bug; it is what "algorithmic bias" actually looks like in practice.

The other surprise was how believable the output feels in favorable cases. The chill_studier profile hit a perfect 7.00/7.00 with just four if-statements and one arithmetic formula. That feels intelligent. But run the same logic on an edge-case profile and it fails instantly in ways a human never would. Real apps feel smarter mostly because their catalog is millions of songs deep — the holes are rarely visible, not because the underlying logic is smarter.

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

