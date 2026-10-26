"""A reproducible color detector with explicit unknown depth."""
import json
import cv2
import numpy as np
from model import ROOT

def detect(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([40, 80, 70]), np.array([85, 255, 255]))
    count, labels, stats, centers = cv2.connectedComponentsWithStats(mask)
    if count <= 1:
        return None
    k = 1+int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    if stats[k, cv2.CC_STAT_AREA] < 100:
        return None
    u, v = centers[k]
    return dict(u=float(u), v=float(v), depth_m=None,
                area_px=int(stats[k, cv2.CC_STAT_AREA]))

if __name__ == '__main__':
    image = np.zeros((240, 320, 3), dtype=np.uint8)
    cv2.circle(image, (210, 110), 20, (0, 255, 0), -1)
    result = detect(image)
    assert result is not None and abs(result['u']-210) < 1
    assert detect(np.zeros_like(image)) is None
    cv2.imwrite(str(ROOT/'logs/object.png'), image)
    (ROOT/'logs/detection.json').write_text(json.dumps(result, indent=2))
    print(result)
