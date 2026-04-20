"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

DIVIDER = "─" * 60

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


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a formatted recommendation block for one user profile."""
    print(f"\n{DIVIDER}")
    print(f"  Profile : {profile_name}")
    print(f"  Genre   : {user_prefs['genre']}  |  Mood: {user_prefs['mood']}")
    print(f"  Energy  : {user_prefs['energy']}  |  Likes acoustic: {user_prefs.get('likes_acoustic', False)}")
    print(DIVIDER)

    recommendations = recommend_songs(user_prefs, songs, k=k)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} — {song['artist']}")
        print(f"      [{song['genre']} / {song['mood']} / energy {song['energy']:.2f}]")
        print(f"      Score : {score:.2f} / 7.00")
        print(f"      Why   : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded {len(songs)} songs from catalog.")

    # Change the key here to switch profiles, or set to None to run all four
    active_profile: str | None = "pop_fan"

    if active_profile:
        print_recommendations(active_profile, PROFILES[active_profile], songs)
    else:
        for name, prefs in PROFILES.items():
            print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
