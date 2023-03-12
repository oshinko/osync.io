import pathlib
import subprocess
import sys

try:
    from PIL import ExifTags, Image
except ModuleNotFoundError:
    subprocess.run(sys.executable + ' -m pip install Pillow', shell=True,
                   check=True)
    from PIL import ExifTags, Image

MAX_WIDTH = 1024
MAX_HEIGHT = 2048

COMPRESS_QUALITY = 85


def f(src_path, dst_dir):
    src_im = Image.open(src_path)
    dst_path = pathlib.Path(dst_dir) / (pathlib.Path(src_path).stem + '.jpg')

    # Exif を削除してから圧縮コピーを保存
    with Image.new(src_im.mode, src_im.size) as dst_im:
        dst_im.putdata(src_im.getdata())
        w, h = dst_im.size

        if w > MAX_WIDTH:
            w, w_ = MAX_WIDTH, w
            h = round(h * w / w_)

        if h > MAX_HEIGHT:
            h, h_ = MAX_HEIGHT, h
            w = round(w * h / h_)

        dst_im.resize((w, h)).save(dst_path, 'JPEG', quality=COMPRESS_QUALITY)


src_dir, dst_dir = sys.argv[1:3]

for path in pathlib.Path(src_dir).iterdir():
    if path.suffix not in ('.jpg', '.jpeg'):
        continue
    f(path, dst_dir)
