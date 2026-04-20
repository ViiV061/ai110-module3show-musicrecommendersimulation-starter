from typing import List, Dict, Tuple
from dataclasses import dataclass
import csv


@dataclass
class Song:
    """Represents a single song with its audio features and metadata."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Stores a listener's taste preferences used for scoring."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Content-based recommender that scores and ranks songs against a UserProfile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the k highest-scoring Song objects for the given user."""
        scored = []
        for song in self.songs:
            score = 0.0
            if song.genre == user.favorite_genre:
                score += 3.0
            if song.mood == user.favorite_mood:
                score += 2.0
            score += 1.5 * (1.0 - abs(song.energy - user.target_energy))
            if user.likes_acoustic and song.acousticness > 0.6:
                score += 0.5
            scored.append((score, song))
        # .sort() mutates the list in-place; fine here since we own `scored`
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why song was recommended to user."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre match (+3.0) — {song.genre}")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match (+2.0) — {song.mood}")
        energy_diff = abs(song.energy - user.target_energy)
        energy_pts = round(1.5 * (1.0 - energy_diff), 2)
        if energy_diff < 0.15:
            reasons.append(f"energy very close (+{energy_pts}) — {song.energy:.2f}")
        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append(f"acoustic match (+0.5) — {song.acousticness:.2f}")
        if not reasons:
            return "discovery pick — outside your usual taste"
        return "; ".join(reasons)


# ---------------------------------------------------------------------------
# Functional API  (used by src/main.py)
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user_prefs and return (total_score, reasons_list).

    Algorithm recipe (max 7.0 points):
      +3.0  genre exact match
      +2.0  mood exact match
      +1.5  energy proximity  — 1.5 × (1 − |user_energy − song_energy|)
      +0.5  acoustic bonus    — only when likes_acoustic and acousticness > 0.6
    """
    score = 0.0
    reasons: List[str] = []

    if song.get("genre") == user_prefs.get("genre"):
        score += 3.0
        reasons.append(f"genre match (+3.0) — {song['genre']}")

    if song.get("mood") == user_prefs.get("mood"):
        score += 2.0
        reasons.append(f"mood match (+2.0) — {song['mood']}")

    user_energy = float(user_prefs.get("energy", 0.5))
    song_energy = float(song.get("energy", 0.5))
    energy_diff = abs(song_energy - user_energy)
    energy_pts = round(1.5 * (1.0 - energy_diff), 2)
    score += energy_pts
    if energy_diff < 0.15:
        reasons.append(f"energy very close (+{energy_pts}) — song={song_energy:.2f}, target={user_energy:.2f}")
    elif energy_diff < 0.30:
        reasons.append(f"energy nearby (+{energy_pts}) — song={song_energy:.2f}, target={user_energy:.2f}")

    if user_prefs.get("likes_acoustic") and float(song.get("acousticness", 0)) > 0.6:
        score += 0.5
        reasons.append(f"acoustic match (+0.5) — {song['acousticness']:.2f}")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top-k results sorted highest to lowest.

    Uses sorted() (returns a new list) instead of .sort() (mutates in-place)
    so the original `songs` catalog is never reordered.
    """
    scored = [
        (song, *score_song(user_prefs, song))   # (song_dict, score, reasons_list)
        for song in songs
    ]
    # sorted() is non-destructive — it leaves `scored` unchanged and returns a new list
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return [
        (song, score, "; ".join(reasons) if reasons else "discovery pick")
        for song, score, reasons in ranked[:k]
    ]
