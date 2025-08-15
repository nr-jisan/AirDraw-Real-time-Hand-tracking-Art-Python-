import cv2
import numpy as np
import mediapipe as mp
import time
from collections import deque

CAM_INDEX = 0
FRAME_W, FRAME_H = 1280, 720
PINCH_THRESHOLD = 0.060  
SMOOTH_ALPHA = 0.45      
INITIAL_BRUSH = 6
MIRROR = True           


PALETTE = {
    '1': (255, 255, 255),  # white
    '2': (255, 0, 0),      # blue
    '3': (0, 255, 0),      # green
    '4': (0, 0, 255),      # red
    '5': (0, 255, 255),    # yellow
    '6': (255, 0, 255),    # magenta
    '7': (255, 255, 0),    # cyan
    '8': (0, 165, 255),    # orange
}


brush_size = INITIAL_BRUSH
brush_color = PALETTE['6'] 
last_pt = None
drawing = False
save_count = 1
fps_hist = deque(maxlen=30)


canvas = np.zeros((FRAME_H, FRAME_W, 4), dtype=np.uint8)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

TEXT_BLACK = (0, 0, 0)

def lerp_point(p, q, a):
    return (int(p[0] + (q[0]-p[0]) * a), int(p[1] + (q[1]-p[1]) * a))

def blend_on_frame(frame_bgr, canvas_rgba):
    """Alpha-blend RGBA strokes onto BGR frame for preview."""
    rgb = canvas_rgba[..., :3].astype(np.float32)
    a = (canvas_rgba[..., 3:4] / 255.0).astype(np.float32)
    base = frame_bgr.astype(np.float32)
    out = base * (1.0 - a) + rgb * a
    return out.astype(np.uint8)

def draw_line_rgba(img, p1, p2, color_bgr, thickness):
    """Draw anti-aliased line onto RGBA canvas while preserving alpha."""
    temp_rgb = np.zeros_like(img[..., :3], dtype=np.uint8)
    temp_a   = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.line(temp_rgb, p1, p2, color_bgr, thickness, lineType=cv2.LINE_AA)
    cv2.line(temp_a,   p1, p2, 255,        thickness, lineType=cv2.LINE_AA)

    a = (temp_a / 255.0)[..., None]
    img_rgb = img[..., :3].astype(np.float32)
    img_a   = img[..., 3:4].astype(np.float32) / 255.0

    new_rgb = img_rgb * (1.0 - a) + temp_rgb.astype(np.float32) * a
    new_a   = np.clip(img_a + a * (1.0 - img_a), 0, 1)

    img[..., :3] = new_rgb.astype(np.uint8)
    img[..., 3]  = (new_a[..., 0] * 255).astype(np.uint8)

def draw_panel_with_text(img, lines, x=10, y=10, pad=8):
    """Light panel behind black text for readability."""
    lh = 22
    w = max(320, max(cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)[0][0] for t in lines) + 2*pad)
    h = lh * len(lines) + 2*pad

    cv2.rectangle(img, (x, y), (x + w, y + h), (230, 230, 230), thickness=-1)
    yy = y + pad + 16
    for t in lines:
        cv2.putText(img, t, (x + pad, yy), cv2.FONT_HERSHEY_SIMPLEX, 0.55, TEXT_BLACK, 1, cv2.LINE_AA)
        yy += lh

def main():
    global last_pt, drawing, brush_size, brush_color, save_count, MIRROR

    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    if not cap.isOpened():
        print("ERROR: Could not open camera.")
        return

    hands = mp_hands.Hands(
        max_num_hands=1,
        model_complexity=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5
    )

    prev_t = time.time()
    hand_detected = False

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        if MIRROR:
            frame = cv2.flip(frame, 1)


        t = time.time()
        fps = 1.0 / max(1e-6, (t - prev_t))
        prev_t = t
        fps_hist.append(fps)

        annotated = frame.copy()


        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(rgb)

        if res.multi_hand_landmarks:
            hand_detected = True
            lms = res.multi_hand_landmarks[0].landmark


            mp_drawing.draw_landmarks(
                annotated,
                res.multi_hand_landmarks[0],
                mp_hands.HAND_CONNECTIONS
            )


            xs = [int(l.x * FRAME_W) for l in lms]
            ys = [int(l.y * FRAME_H) for l in lms]
            x1, y1, x2, y2 = max(0, min(xs)), max(0, min(ys)), min(FRAME_W-1, max(xs)), min(FRAME_H-1, max(ys))
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (40, 220, 40), 2)


            p_thumb = lms[4]
            p_index = lms[8]
            d = ((p_thumb.x - p_index.x)**2 + (p_thumb.y - p_index.y)**2) ** 0.5
            drawing = d < PINCH_THRESHOLD


            x = int(p_index.x * FRAME_W)
            y = int(p_index.y * FRAME_H)
            target = (x, y)

            if last_pt is None:
                last_pt = target
            smoothed = lerp_point(last_pt, target, SMOOTH_ALPHA)

            if drawing:
                draw_line_rgba(canvas, last_pt, smoothed, brush_color, brush_size)

            cv2.circle(annotated, smoothed, 6, (0, 0, 0), -1)  # black
            last_pt = smoothed
        else:
            hand_detected = False
            last_pt = None
            drawing = False


        preview = blend_on_frame(annotated, canvas)


        mean_fps = int(sum(fps_hist)/max(1, len(fps_hist)))
        status = "Hand: DETECTED" if hand_detected else "Hand: NOT DETECTED"
        lines = [
            f"{status}   |   {mean_fps} fps",
            "Pinch thumb+index to draw",
            "[1-8] color  [+/-] size  [c] clear  [s] save PNG",
            "[m] mirror  [q] quit   Brush: {}px".format(brush_size)
        ]
        draw_panel_with_text(preview, lines, x=10, y=10)

        cv2.imshow("AirDraw — Python (preview)", preview)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key in map(ord, '12345678'):
            brush_color = PALETTE[chr(key)]
        elif key in (ord('+'), ord('=')):
            brush_size = min(48, brush_size + 1)
        elif key in (ord('-'), ord('_')):
            brush_size = max(1, brush_size - 1)
        elif key == ord('c'):
            canvas[:] = 0
            last_pt = None
        elif key == ord('s'):
            fname = f"airdraw_{save_count:03d}.png"
            cv2.imwrite(fname, canvas)
            print(f"Saved {fname}")
            save_count += 1
        elif key == ord('m'):
            MIRROR = not MIRROR

    hands.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




    



