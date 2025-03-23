# Source paper: https://arxiv.org/pdf/2002.11331
# Should have more optimal security properties than a typical linear feedback shift register
# If implemented in C, it should also have very low register pressure (i.e. be extremely performant)
def rotl64(d, lrot):
    return ((d << lrot) | (d >> (64 - lrot))) & 0xFFFFFFFFFFFFFFFF

class RomuQuad:
    def __init__(self, seed):
        self.wState = (seed >> 192) & 0xFFFFFFFFFFFFFFFF
        self.xState = (seed >> 128) & 0xFFFFFFFFFFFFFFFF
        self.yState = (seed >> 64) & 0xFFFFFFFFFFFFFFFF
        self.zState = seed & 0xFFFFFFFFFFFFFFFF

        if self.wState == 0:
            self.wState = 1
        if self.xState == 0:
            self.xState = 1
        if self.yState == 0:
            self.yState = 1
        if self.zState == 0:
            self.zState = 1

    def random(self):
        wp = self.wState
        xp = self.xState
        yp = self.yState
        zp = self.zState

        self.wState = (0xD3833E804055490B * zp) & 0xFFFFFFFFFFFFFFFF
        self.xState = (zp + rotl64(wp, 52)) & 0xFFFFFFFFFFFFFFFF
        self.yState = (yp - xp) & 0xFFFFFFFFFFFFFFFF
        temp_z = (yp + wp) & 0xFFFFFFFFFFFFFFFF
        self.zState = rotl64(temp_z, 19)

        return xp