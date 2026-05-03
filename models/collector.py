# models/collector.py

from models.album import Album


class Collector:
    """Representa a un coleccionador con su álbum y su historial de compras."""

    def __init__(self, name: str):
        self.name = name
        self.album = Album()
        self.packs_opened = 0
        self.final_duplicates = None  # None hasta que complete el álbum

    def buy_pack(self):
        """Compra y abre un sobre."""
        self.album.open_pack()
        self.packs_opened += 1

        # Registramos las duplicadas justo cuando completa
        if self.album.is_complete and self.final_duplicates is None:
            self.final_duplicates = len(self.album.duplicates)

    def give_stickers(self, stickers: list):
        """
        Entrega estampillas de sus repetidas hacia un intercambio.
        Remueve las estampillas dadas de su lista de duplicates.
        """
        for sticker in stickers:
            self.album.duplicates.remove(sticker)

    def receive_stickers(self, stickers: list):
        for sticker in stickers:
            if sticker in self.album.needed:
                self.album.needed.remove(sticker)
            else:
                self.album.duplicates.append(sticker)

        # Por si completa el álbum vía intercambio
        if self.album.is_complete and self.final_duplicates is None:
            self.final_duplicates = len(self.album.duplicates)

    @property
    def is_complete(self):
        return self.album.is_complete

    @property
    def packs_opened(self):
        return self._packs_opened

    @packs_opened.setter
    def packs_opened(self, value):
        self._packs_opened = value

    def __repr__(self):
        return (f"Collector({self.name}, "
                f"sobres={self.packs_opened}, "
                f"{self.album})")