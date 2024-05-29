from typing import Iterable
import tarfile
from pathlib import Path
import os

from .base import ArchivalRepository
from .io import PartialReader
from ...cache import CACHE
from ...commons import logger


class TarRepository(ArchivalRepository):

    _warmed_up = False

    def __init__(self, path: str, *args, gzip=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.path = path
        self.reader = PartialReader(path)

        self.reader.open()
        self.gzip = gzip

        # random access on gzip
        if self.gzip:
            self.warmup()

    @property
    def unpacked_dir(self):
        dirname = CACHE.build_filename(self.path, ".unpacked")
        dirpath = Path(dirname)
        return dirpath

    def close(self):
        self.reader.close()

    def ls(self):
        if self._warmed_up:
            assert self.unpacked_dir.is_dir()
            yield from [
                f"{dirpath}/{filename}"
                for dirpath, dirnames, filenames in os.walk(self.unpacked_dir)
                for filename in filenames
            ]
            return

        if self.gzip:
            logger.warning("tararchive is gzipped. Random access can be quite slow.")
        fh = tarfile.open(fileobj=self.reader, mode=("r:gz" if self.gzip else "r"))
        for mem in fh.getmembers():
            yield mem.name

    def warmup(self, *args, **kwargs):
        if self._warmed_up:
            return
        self.reader.warmup()
        fh = tarfile.open(fileobj=self.reader, mode=("r:gz" if self.gzip else "r"))
        assert (
            not self.unpacked_dir.is_file()
        ), f"{str(self.unpacked_dir)} is a file. Abort."
        if not self.unpacked_dir.is_dir():
            self.unpacked_dir.mkdir(parents=True)
        fh.extractall(self.unpacked_dir)
        self._warmed_up = True

    def get(self, filename: str) -> bytes:

        if self.gzip:
            self.warmup()

        if self._warmed_up:
            filepath = self.unpacked_dir / filename
            if filepath.is_file():
                return filepath.read_bytes()
            raise FileNotFoundError(f"{filename} not found.")

        if self.gzip:
            logger.warning("tararchive is gzipped. Random access can be quite slow.")

        fh = tarfile.open(fileobj=self.reader, mode=("r:gz" if self.gzip else "r"))
        try:
            extracted = fh.extractfile(filename)
            return extracted.read()
        except KeyError as e:
            raise FileNotFoundError(f"{filename} not found.") from e

    def search_files(self, prefix: str) -> Iterable[str]:
        return super().search_files(prefix)
