from pathlib import Path
import shutil


script = Path("basilisk_mockup/main.py")
shutil.copy(script, Path("dist3/Basilisk"))
