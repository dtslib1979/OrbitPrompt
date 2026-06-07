# fastText numpy 2.x 호환성 패치
import fasttext as _ft
import numpy as _np
_orig = _ft.FastText.FastText.predict
_ft.FastText.FastText.predict = lambda self, text, k=1, t=0.0: (
    lambda r: (r[0], _np.asarray(r[1], dtype=float)) 
)(_orig(self, text, k, t))
