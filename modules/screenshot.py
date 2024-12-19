import mss
import numpy as np

class ScreenshotManager:
    def __init__(self):
        self.sct = mss.mss()
        self.path = None

    def __del__(self):
        self.sct.close()

    def capture(self, top, left, width, height) -> np.array:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        
        sct_img = self.sct.grab(monitor)
        
        img_np = np.array(sct_img)[:, :, :3] 

        return img_np