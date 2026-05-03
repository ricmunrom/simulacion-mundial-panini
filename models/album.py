# models/album.py

import random
from config import ALBUM_SIZE, STICKERS_PER_PACK


class Album:
    """Representa el álbum de un coleccionador."""

    def __init__(self):
        self.needed = set(range(ALBUM_SIZE))      # Estampillas que faltan
        self.duplicates = []                       # Estampillas repetidas (intercambiables)

    def open_pack(self):
        """Abre un sobre y agrega las estampillas al álbum."""
        pack = random.sample(range(ALBUM_SIZE), STICKERS_PER_PACK)

        for sticker in pack:
            if sticker in self.needed:
                self.needed.remove(sticker)
            else:
                self.duplicates.append(sticker)

    @property
    def is_complete(self):
        """Regresa True si el álbum está lleno."""
        return len(self.needed) == 0

    @property
    def completion_pct(self):
        """Porcentaje de llenado del álbum."""
        return round((ALBUM_SIZE - len(self.needed)) / ALBUM_SIZE * 100, 2)

    def __repr__(self):
        return (f"Album(completado={self.completion_pct}%, "
                f"faltan={len(self.needed)}, "
                f"repetidas={len(self.duplicates)})")