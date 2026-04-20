"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

DIVIDER = "─" * 60

# ── Standard profiles ────────────────────────────────────────────────────────

PROFILES = {
    "pop_fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    },
    "chill_studier": {
        "genre": "lofi",
        "mood": "focused",
        "energy": 0.4,
        "likes_acoustic": True,
    },
    "hard_rocker": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "likes_acoustic": False,
    },
    "r&b_romantic": {
        "genre": "r&b",
        "mood": "romantic",
        "energy": 0.6,
        "likes_acoustic": False,
    },
}

# ── Adversarial / edge-case profiles ────────────────────────────────────────

ADVERSARIAL = {
    # Conflict: metal genre + melancholic mood are almost never paired in the catalog
    "grief_workout": {
        "genre": "metal",
        "mood": "melancholic",
        "energy": 0.92,
        "likes_acoustic": False,
    },
    # Sparse coverage: only one classical song exists in the catalog
    "classical_student": {
        "genre": "classical",
        "mood": "focused",
        "energy": 0.25,
        "likes_acoustic": True,
    },
    # Extreme signals: very low energy + acoustic — tests whether acoustic bonus
    # can compete with genre/mood mismatches
    "extreme_acoustic": {
        "genre": "folk",
        "mood": "melancholic",
        "energy": 0.15,
        "likes_acoustic": True,
    },
    # Genre void: jazz fan who wants intense/high-energy — the only jazz song is
    # "relaxed", so genre and mood signals point in opposite directions
    "jazz_intensity": {
        "genre": "jazz",
        "mood": "intense",
        "energy": 0.85,
        "likes_acoustic": False,
    },
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def print_recommendations(
    profile_name: str,
    user_prefs: dict,
    songs: list,
    k: int = 5,
    **weights,
) -> None:
    """Print a formatted recommendation block for one user profile."""
    label = f"  Profile : {profile_name}"
    if weights:
        wlabel = ", ".join(f"{k}={v}" for k, v in weights.items())
        label += f"  [weights: {wlabel}]"
    print(f"\n{DIVIDER}")
    print(label)
    print(f"  Genre   : {user_prefs['genre']}  |  Mood: {user_prefs['mood']}")
    print(f"  Energy  : {user_prefs['energy']}  |  Likes acoustic: {user_prefs.get('likes_acoustic', False)}")
    print(DIVIDER)

    for rank, (song, score, explanation) in enumerate(
        recommend_songs(user_prefs, songs, k=k, **weights), start=1
    ):
        print(f"  #{rank}  {song['title']} — {song['artist']}")
        print(f"      [{song['genre']} / {song['mood']} / energy {song['energy']:.2f}]")
        print(f"      Score : {score:.2f}  |  Why: {explanation}")
        print()


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded {len(songs)} songs from catalog.")

    # ── Standard profiles ──────────────────────────────────────────────────
    print("\n══ STANDARD PROFILES ══")
    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)

    # ── Adversarial / edge-case profiles ──────────────────────────────────
    print("\n══ ADVERSARIAL PROFILES ══")
    for name, prefs in ADVERSARIAL.items():
        print_recommendations(name, prefs, songs)

    # ── Weight experiment: halve genre, double energy ──────────────────────
    print("\n══ WEIGHT EXPERIMENT (pop_fan) ══")
    print("  Comparing default weights vs. genre_w=1.5 / energy_w=3.0\n")
    print_recommendations("pop_fan  [DEFAULT  genre=3.0, energy=1.5]",
                           PROFILES["pop_fan"], songs, k=5)
    print_recommendations("pop_fan  [EXPERIMENT genre=1.5, energy=3.0]",
                           PROFILES["pop_fan"], songs, k=5,
                           genre_w=1.5, energy_w=3.0)


if __name__ == "__main__":
    main()
