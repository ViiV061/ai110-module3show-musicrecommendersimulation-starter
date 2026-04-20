# Reflection: Profile Comparisons

## pop_fan vs. chill_studier

**pop_fan** (genre=pop, mood=happy, energy=0.8) and **chill_studier** (genre=lofi, mood=focused, energy=0.4, likes_acoustic=True) produce completely non-overlapping top-5 lists — not a single song appears in both. The pop_fan's top result is Sunrise City (6.47/7), which scores because it hits all three main signals: genre, mood, and energy proximity. The chill_studier achieves a perfect 7.00/7.00 with Focus Flow because every feature matched exactly, including the acoustic bonus.

This makes sense: these two profiles represent genuinely different vibes — bright and danceable pop versus low-energy background study music. The scoring behaves as expected. What is worth noting is that the chill_studier's #4 result is "Late Night Cipher" (hip-hop / focused, 3.16), which ranked high purely on the mood "focused" match. A real listener might not expect hip-hop to appear in a lofi study list, but the system has no concept of sonic similarity — it only sees the mood label.

---

## hard_rocker vs. r&b_romantic

**hard_rocker** (genre=rock, mood=intense, energy=0.92) gets a coherent and intuitive top 3: Storm Runner (rock/intense), Gym Hero (pop/intense), and Iron Curtain (metal/intense). Positions #4 and #5 score only 1.46 — pure energy proximity with no genre or mood match. The system correctly finds the intense-high-energy cluster.

**r&b_romantic** (genre=r&b, mood=romantic, energy=0.6) tells a very different story. Velvet Signal (r&b/romantic, 6.48) is a strong #1, but then the score collapses: positions #2–5 all score below 1.5 because only one r&b song exists and no other song is labeled "romantic." The system has nothing else to offer. The gap between #1 (6.48) and #2 (1.47) is enormous — a 5-point drop — which signals that this user is poorly served by the catalog. In a real product, this is the user who churns because the app keeps recommending irrelevant songs after the first one.

---

## classical_student vs. grief_workout (adversarial)

**classical_student** (genre=classical, mood=focused, energy=0.25, likes_acoustic=True) exposes the sparse coverage problem. Nocturne in Blue is the only classical song and it scores 4.96 despite a mood mismatch (it is "melancholic", not "focused"). Position #2 drops to a lofi song (Focus Flow, 3.77) because the mood "focused" exists there. The system cannot distinguish a classical piano student from a lofi study listener — both end up with lofi as the backup genre.

**grief_workout** (genre=metal, mood=melancholic, energy=0.92) is a deliberately contradictory profile. Metal songs in the catalog are labeled "intense", so the only metal song (Iron Curtain) wins on genre but misses on mood. The system then ranks Campfire Letter (folk/melancholic) at #2 — an acoustic folk song for someone wanting high-energy metal. The energy signals conflict with the mood signals so severely that the output feels random. This shows that when a user's preferences are internally inconsistent with the catalog's labeling scheme, the system cannot produce a meaningful recommendation.

---

## extreme_acoustic vs. jazz_intensity (adversarial)

**extreme_acoustic** (genre=folk, mood=melancholic, energy=0.15, likes_acoustic=True) is actually the best-served adversarial profile. Campfire Letter (folk/melancholic, 0.94 acousticness) scores 6.76 — a near-perfect result. The genre and mood both exist in the catalog, so the system works as intended. The interesting part is positions #2–5: Nocturne in Blue, Spacewalk Thoughts, Library Rain, and Coffee Shop Stories — all very different genres but united by low energy and high acousticness. The acoustic bonus acts as a tiebreaker that surfaces a coherent low-energy, textured-sound cluster.

**jazz_intensity** (genre=jazz, mood=intense, energy=0.85) is the clearest system failure observed in testing. Coffee Shop Stories ranks #1 (3.78) even though it is a relaxed, low-energy jazz song that is the opposite of what the user described. The genre weight (3.0) alone carries it to the top over three songs that correctly match the mood and energy but have the wrong genre (#2 Storm Runner, #3 Gym Hero, #4 Iron Curtain, all around 3.4). A real listener playing this recommendation would immediately skip it, yet the system would give the same wrong answer on every session. This is the most concrete example of how a transparent but simple scoring rule can fail users with nuanced or underrepresented taste combinations.

---

## Weight Experiment: pop_fan default vs. genre_w=1.5 / energy_w=3.0

Halving the genre weight and doubling the energy weight shifted the pop_fan ranking in a revealing way. Gym Hero (pop/intense, energy=0.93) dropped from #2 to #5. Why? With default weights, Gym Hero earned 3.0 genre points that gave it a large buffer despite the mood mismatch. With the experiment weights, that buffer shrank to 1.5 and Gym Hero's energy score only partially compensated. Meanwhile, Rooftop Lights (indie pop/happy, energy=0.76) rose from #3 to #2 and Neon Heartbeat (k-pop/happy, energy=0.89) rose to #3, because their happy mood match (2.0) plus strong energy proximity (now worth up to 3.0) outweighed Gym Hero's weakened genre advantage. The experiment makes intuitive sense: if you care more about energy than genre, a song from a different genre that matches your vibe perfectly should rank higher than a same-genre song that is energetically off. The default weights are more conservative and genre-centric; the experimental weights reward cross-genre discovery at the cost of genre specificity.
