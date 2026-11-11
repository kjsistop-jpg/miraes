"""index.html에 쓰인 글자만 담은 글꼴 파일을 assets/fonts에 만든다.
문구를 고친 뒤에는 이 스크립트를 다시 실행해야 새 글자가 같은 글꼴로 보인다.
원본: Noto Sans/Serif CJK KR (SIL Open Font License)."""
import re, sys, pathlib
from fontTools.ttLib import TTCollection
from fontTools import subset
root = pathlib.Path(__file__).resolve().parent.parent
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/usr/share/fonts/opentype/noto')
html = (root / 'index.html').read_text(encoding='utf-8')
html = re.sub(r'<(script|style)\b.*?</\1>', ' ', html, flags=re.S)
chars = set(html) | set(map(chr, range(0x20, 0x7f))) | set('“”‘’·…×—–→↑©℡㈜①②③④⑤⑥⑦⑧⑨⑩')
chars |= set('가나다라마바사아자차카타파하년월일시분호번지층동읍면리로길')
text = ''.join(sorted(c for c in chars if ord(c) >= 0x20))
jobs = [('NotoSerifCJK-SemiBold.ttc', 'Noto Serif CJK KR', 'serif-600'),
        ('NotoSerifCJK-Medium.ttc', 'Noto Serif CJK KR', 'serif-500'),
        ('NotoSansCJK-Regular.ttc', 'Noto Sans CJK KR', 'sans-400'),
        ('NotoSansCJK-Medium.ttc', 'Noto Sans CJK KR', 'sans-500'),
        ('NotoSansCJK-Bold.ttc', 'Noto Sans CJK KR', 'sans-700')]
for file, family, out in jobs:
    col = TTCollection(str(src / file))
    font = next(f for f in col.fonts if f['name'].getDebugName(1).startswith(family) and 'Mono' not in f['name'].getDebugName(1))
    opt = subset.Options(); opt.flavor = 'woff'; opt.hinting = False; opt.desubroutinize = True
    opt.layout_features = ['kern', 'liga', 'locl', 'ccmp', 'mark', 'mkmk']; opt.name_IDs = [1, 2]; opt.notdef_outline = True
    s = subset.Subsetter(opt); s.populate(text=text); s.subset(font)
    font.flavor = 'woff'; dst = root / 'assets' / 'fonts' / (out + '.woff'); font.save(str(dst))
    print(out, len(text), 'chars', dst.stat().st_size // 1024, 'KB')
