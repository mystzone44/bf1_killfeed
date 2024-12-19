import mss
import numpy as np

def capture(dimensions) -> np.array:
    with mss.mss() as sct:
        left, top, width, height = dimensions
        monitor = {"top": top, "left": left, "width": width, "height": height}
        
        sct_img = sct.grab(monitor)
        
        img_np = np.array(sct_img)[:, :, :3] 

    return img_np