"""Build and validate the Foundry release ZIP, manifest and checksums.

Usage: python tools/package_release.py
This packages the existing final module; it does not generate artwork.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULE = ROOT / "n5eb-feux-follets"
REPOSITORY = "https://github.com/PrevotYann/one-shots-n5eb"


def main():
    manifest = json.loads((MODULE / "module.json").read_text(encoding="utf-8"))
    version = manifest["version"]
    tag = f"v{version}"
    if not version or any(c not in "0123456789.-abcdefghijklmnopqrstuvwxyz" for c in version):
        raise ValueError("Invalid release version")
    if manifest["id"] != MODULE.name:
        raise ValueError("Module directory must match its manifest id")
    if manifest["manifest"] != f"{REPOSITORY}/releases/latest/download/module.json":
        raise ValueError("Unexpected stable manifest URL")
    archive_name = f"{MODULE.name}.zip"
    if manifest["download"] != f"{REPOSITORY}/releases/download/{tag}/{archive_name}":
        raise ValueError("Download URL does not match release version and ZIP name")
    # Build in a separate process so all image references resolve against the
    # packaged files, then run the complete final-art contract checks.
    subprocess.run([sys.executable, str(ROOT / "tools/build.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "tools/validate_art.py")], cwd=ROOT, check=True)
    adventure = json.loads((MODULE / "data/adventure.json").read_text(encoding="utf-8"))
    if adventure["version"] != version:
        raise ValueError("Module and adventure versions differ")
    out = ROOT / "output" / tag
    out.mkdir(parents=True, exist_ok=True)
    archive_path = out / archive_name
    files = sorted(file for file in MODULE.rglob("*") if file.is_file())
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for file in files:
            relative = file.relative_to(MODULE)
            if file.is_symlink() or any(part.startswith(".") or part == "__pycache__" for part in relative.parts):
                raise ValueError(f"Unexpected runtime file: {relative}")
            # Foundry archive root is the module root, not a repository snapshot.
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, file.read_bytes(), compresslevel=6)
    shutil.copyfile(MODULE / "module.json", out / "module.json")
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise ValueError("Corrupt release ZIP")
        expected = {file.relative_to(MODULE).as_posix() for file in files}
        if set(archive.namelist()) != expected or "module.json" not in expected:
            raise ValueError("Incorrect ZIP layout")
        if archive.read("module.json") != (out / "module.json").read_bytes():
            raise ValueError("Attached manifest differs from packaged manifest")
        for file in files:
            if archive.read(file.relative_to(MODULE).as_posix()) != file.read_bytes():
                raise ValueError(f"ZIP file differs from source: {file}")
    sums = "".join(f"{hashlib.sha256((out / name).read_bytes()).hexdigest()}  {name}\n"
                   for name in (archive_name, "module.json"))
    (out / "SHA256SUMS.txt").write_text(sums, encoding="utf-8", newline="\n")
    print(f"Release {tag}: {len(files)} module files -> {archive_path}")
    print(f"Manifest and SHA256SUMS.txt -> {out}")


if __name__ == "__main__":
    main()
