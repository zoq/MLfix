# AUTOGENERATED! DO NOT EDIT! File to edit: A. Downsize images.ipynb (unless otherwise specified).

__all__ = ['downsize_images']

# Internal Cell
from fastai.vision.all import *
from fastcore.script import *

# Internal Cell
def resize_image(file, path, dest, max_size=None, n_channels=3, ext=None,
                 img_format=None, resample=Image.BILINEAR, resume=False, **kwargs ):
    "Resize file to dest to max_size"
    dest = Path(dest)
    dest_fname = dest/os.path.relpath(file, path)
    os.makedirs(dest_fname.parent, exist_ok=True)
    if resume and dest_fname.exists(): return
    if verify_image(file):
        img = Image.open(file)
        imgarr = np.array(img)
        img_channels = 1 if len(imgarr.shape) == 2 else imgarr.shape[2]
        if (max_size is not None and (img.height > max_size or img.width > max_size)) or img_channels != n_channels:
            if ext is not None: dest_fname=dest_fname.with_suffix(ext)
            if max_size is not None:
                new_sz = resize_to(img, max_size)
                img = img.resize(new_sz, resample=resample)
            if n_channels == 3: img = img.convert("RGB")
        img.save(dest_fname, img_format, **kwargs)

def resize_images(path, max_workers=defaults.cpus, max_size=None, recurse=False,
                  dest=Path('.'), n_channels=3, ext=None, img_format=None, resample=Image.BILINEAR,
                  resume=None, progress=True, **kwargs):
    "Resize files on path recursively to dest to max_size"
    path = Path(path)
    if resume is None and dest != Path('.'): resume=False
    os.makedirs(dest, exist_ok=True)
    files = get_image_files(path, recurse=recurse)
    parallel(resize_image, files, path=path, max_workers=max_workers, max_size=max_size, dest=dest,
             n_channels=n_channels, ext=ext, img_format=img_format, resample=resample, resume=resume,
             progress=progress, **kwargs)

# Cell
@call_parse
def downsize_images(
        indir:Path,  # folder with images
        outdir:Path, # output folder
        max_size:int=256, # maximum size of the longest edge
    ):
    """Resizes a folder of images so the longest edge is shorter than max_size.
    Preserves nested directory structure."""
    if len(get_image_files(indir)) == 0:
        raise Exception(f"No image files found in: {indir}!")
    resize_images(indir, max_size=max_size, dest=outdir, ext='.jpg', recurse=True, progress=True)