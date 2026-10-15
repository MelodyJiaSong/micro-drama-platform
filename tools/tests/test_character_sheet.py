from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from character_sheet import compose
from PIL import Image


def test_triptych_preserves_pixels_and_direction_with_mixed_sizes(tmp_path: Path) -> None:
    original = []
    for role,size,color in zip(('front','side','back'),((5,9),(7,4),(3,6)),('red','green','blue')):
        im = Image.new('RGB',size,color)
        im.save(tmp_path/f'c1_Test_{role}.png')
        original.append(im)
    row = compose(tmp_path,'c1_Test')
    with Image.open(row['path']) as image:
        assert image.size == (21,9)
        for i,im in enumerate(original):
            x,y = i*7+(7-im.width)//2,(9-im.height)//2
            assert image.crop((x,y,x+im.width,y+im.height)).tobytes() == im.tobytes()
    assert compose(tmp_path,'c1_Test')['status'] == 'current'
