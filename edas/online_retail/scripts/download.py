"""Descarga pública versionada, verifica integridad y extrae solo XLSX esperados."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://archive.ics.uci.edu/static/public/352/online+retail.zip'
SHA256 = 'f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b'
FILES = ['Online Retail.xlsx']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--force', action='store_true', help='Volver a descargar el ZIP')
    args = parser.parse_args()
    data = ROOT / 'data'
    raw = data / 'raw'
    raw.mkdir(parents=True, exist_ok=True)
    archive = data / 'online-retail.zip'
    if args.force or not archive.exists():
        partial = archive.with_suffix('.part')
        try:
            subprocess.run(['curl', '-fL', '--retry', '3', '--connect-timeout', '30',
                            '--max-time', '300', '-o', str(partial), URL], check=True)
            with partial.open('rb') as handle:
                digest = hashlib.file_digest(handle, 'sha256').hexdigest()
            if digest != SHA256:
                raise ValueError('SHA-256 inesperado: no se aceptará otra versión ni una página de acceso.')
            partial.replace(archive)
        finally:
            partial.unlink(missing_ok=True)
    with archive.open('rb') as handle:
        digest = hashlib.file_digest(handle, 'sha256').hexdigest()
    if digest != SHA256:
        raise ValueError('ZIP local corrupto o diferente. Ejecuta con --force.')
    with zipfile.ZipFile(archive) as bundle:
        if set(bundle.namelist()) != set(FILES):
            raise ValueError('Contenido del ZIP diferente al esperado.')
        if bundle.testzip() is not None:
            raise ValueError('Falló la comprobación CRC del ZIP.')
        for name in FILES:
            (raw / name).write_bytes(bundle.read(name))
        metadata = dict(url=URL, version="UCI 352", sha256=digest,
                        compressed_bytes=archive.stat().st_size,
                        uncompressed_bytes=sum(i.file_size for i in bundle.infolist()),
                        files=FILES, license='CC BY 4.0')
    (data / 'manifest.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(f'Verificados y extraídos {len(FILES)} XLSX. SHA-256: {digest}')


if __name__ == '__main__':
    main()
