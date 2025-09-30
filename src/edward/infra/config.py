import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    repo_root: Path
    assets_dir: Path
    maps_dir: Path
    images_dir: Path

    @staticmethod
    def from_env() -> "Settings":
        # src/edward/infra/config.py -> parents[3] = repo root
        root = Path(__file__).resolve().parents[3]
        assets = root / "assets"
        return Settings(
            repo_root=root,
            assets_dir=assets,
            maps_dir=assets / "maps",
            images_dir=assets / "images",
        )