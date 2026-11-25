"""Compare the Ebb Cantor review frames, register the printed seam, and verify packaged bytes."""
from pathlib import Path
import hashlib
import json
import tarfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "unity-validation/Assets"
OUTFIT = ASSETS / "NightcapDarkElfFemale/ebb-cantor"
SOURCE = ROOT / "output/dark-elf-female/ebb-cantor"
REVIEW = SOURCE / "UnityReview"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def photo(name):
    return Image.open(REVIEW / (name + ".png")).convert("RGB")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def difference(first, second):
    a, b = [np.asarray(photo(n), dtype=np.int16) for n in (first, second)]
    diff = np.abs(a - b)
    return dict(mean=float(diff.mean()), p99=float(np.percentile(diff, 99)),
                maximum=int(diff.max()), changed_pixels=float(np.any(diff, axis=2).mean()))


def font(size, bold=False):
    try:
        return ImageFont.truetype("segoeuib.ttf" if bold else "segoeui.ttf", size)
    except OSError:
        return ImageFont.load_default(size=size)


def board(filename, title, shots, tile):
    w, h = tile
    gap, margin = 8, 22
    page = Image.new("RGB", (2*margin + len(shots)*w + (len(shots)-1)*gap,
                            h+130), "#222329")
    draw = ImageDraw.Draw(page)
    draw.text((margin, 14), title, font=font(31, True), fill="#f3eee1")
    for i, (label, im) in enumerate(shots):
        x = margin + i*(w+gap)
        im = im.copy()
        im.thumbnail(tile, Image.Resampling.LANCZOS)
        page.paste(im, (x+(w-im.width)//2, 64+(h-im.height)//2))
        draw.text((x, 74+h), label, font=font(19), fill="#ded4c1")
    page.save(REVIEW/filename, quality=94)


def package_check():
    dependencies = set((REVIEW/"scene-dependencies.txt").read_text().splitlines())
    with tarfile.open(REVIEW/"Ebb-Cantor.unitypackage", "r:gz") as package:
        files = {entry.name.strip("./"): entry for entry in package.getmembers() if entry.isfile()}
        packaged = set()
        for member in files:
            guid, _, name = member.partition("/")
            if name != "pathname":
                continue
            path = package.extractfile(files[member]).read().decode().strip("\x00\r\n")
            target = ASSETS.parent/path
            if target.is_file():
                assert target.read_bytes() == package.extractfile(files[guid+"/asset"]).read(), path
                assert Path(str(target)+".meta").read_bytes() == package.extractfile(files[guid+"/asset.meta"]).read(), path
                packaged.add(path)
        assert all(path in packaged for path in dependencies if path.startswith("Assets/"))
        return len(packaged)


def main():
    audit = read_json(REVIEW/"import-audit.json")
    play = read_json(REVIEW/"play-audit.json")
    avatar = read_json(REVIEW/"avatar-configuration.json")
    source = read_json(SOURCE/"Review/FBX-roundtrip.json")
    assert audit["passed"] and play["passed"] and len(avatar["assigned"]) == 52
    assert play["stationaryFrames"] >= 12 and play["jointDriftMetres"] == 0
    assert digest(SOURCE/"DarkElfFemale.fbx") == digest(OUTFIT/"Model/DarkElfFemale.fbx")
    for m in audit["textures"]:
        name = m["name"]+".png"
        assert digest(SOURCE/"Textures"/name) == digest(OUTFIT/"Textures"/name)
        assert Image.open(SOURCE/"Textures"/name).size == (m["size"],m["height"])
        assert m["format"] == "BC7" and m["sRGB"] and m["mips"] > 1
    for mesh in audit["meshes"]:
        original = source["meshes"][mesh["name"]]
        assert mesh["triangles"] == original["triangles"]
        assert mesh["material"].split(" / ") == [s.split(" | ")[1] for s in original["material_slots"]]
    metrics = dict(fbx_sha256=digest(SOURCE/"DarkElfFemale.fbx"),
                   verified_package_files=package_check(),
                   edit_vs_play=difference("Edit-mode","Play-mode"),
                   bc7_face=difference("Face-before-compression","Face-collar"),
                   bc7_procession=difference("Hem-before-compression","Procession-seam"))
    assert metrics["edit_vs_play"]["maximum"] == 0
    (REVIEW/"comparison.json").write_text(json.dumps(metrics,indent=2)+"\n")
    board("Ebb-Cantor-in-Unity.jpg", "Ebb Cantor", [
        ("Neutral studio",photo("Neutral-three-quarter")),("Reversed key",photo("Reversed-key")),
        ("Cool dusk and lamplight",photo("Dusk"))],(400,460))
    raw = photo("Procession-seam")
    marked = raw.copy()
    points = np.loadtxt(REVIEW/"hem-seam.tsv")
    ImageDraw.Draw(marked).line([tuple(pt) for pt in points], fill="#43d7dc", width=3)
    board("Printed-seam.jpg","Funeral procession",[
        ("Printed hem in Unity",raw),("Shared edge of the front and east panels",marked)],(580,435))


if __name__ == "__main__":
    main()

