"""Shared publication typography; font files stay on the local machine."""
from pathlib import Path
import hashlib
import matplotlib as mpl
from matplotlib import font_manager as fm

FAMILY = 'Comic Sans MS'


def configure(size=7.4):
    # Register both faces explicitly: Matplotlib's cached macOS inventory may
    # predate this font. PDFs embed subsets; SVGs use paths for portable display.
    for directory in [Path('/System/Library/Fonts/Supplemental'),
                      Path('/Library/Fonts'), Path.home()/'Library/Fonts']:
        if directory.exists():
            for path in directory.glob('**/*'):
                if path.suffix.lower() in {'.ttf', '.otf'} and 'comic' in path.name.lower():
                    fm.fontManager.addfont(str(path))
    faces = {}
    for weight in ['normal', 'bold']:
        path = Path(fm.findfont(fm.FontProperties(family=FAMILY, weight=weight),
                               fallback_to_default=False))
        face = fm.FontProperties(fname=str(path))
        if face.get_name() != FAMILY:
            raise RuntimeError(f'{FAMILY} {weight} is required; found {face.get_name()}')
        faces[weight] = dict(file=path.name,
                             sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    if faces['normal']['sha256'] == faces['bold']['sha256']:
        raise RuntimeError('Install the separate Comic Sans MS Bold face.')
    mpl.rcParams.update({'font.family': FAMILY, 'font.size': size,
                         'pdf.fonttype': 42, 'ps.fonttype': 42,
                         'svg.fonttype': 'path', 'axes.unicode_minus': False})
    return dict(family=FAMILY, faces=faces, pdfEmbedded=True, svgTextAsPaths=True)
