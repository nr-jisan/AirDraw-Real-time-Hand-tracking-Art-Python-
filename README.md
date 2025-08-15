<h1 align="center">🎨 AirDraw — Real-Time Hand-Tracking Art (Python)</h1>

<h2 align="center">
  <img src="https://readme-typing-svg.demolab.com/?lines=Draw+in+the+Air+with+Your+Hand!;OpenCV+%2B+MediaPipe+%2B+Python;Undo%2FRedo+.+Color+Palette+.+PNG+Export!&center=true&width=500&height=30&color=58A6FF&vCenter=true&size=20" />
</h2>

<p align="center">
  ✨ A touchless drawing app: pinch your <b> thumb + index </b> in front of the camera to paint on a transparent canvas, change colors, undo/redo, and save as PNG — all in real time.
</p>

<p align="center">
  <img src="https://media.giphy.com/media/qgQUggAC3Pfv687qPC/giphy.gif" width="350" alt="demo placeholder"/>
  <br/><em>(Replace this GIF with your own demo if you like.)</em>
</p>

---

## 📌 Features

✅ Pinch-to-draw (thumb tip ↔ index tip distance)  
✅ **Undo / Redo** (Z/U & Y/R)  
✅ **Clickable color palette** + keys **1–8**  
✅ Brush size control (**+ / -**)  
✅ **Transparent PNG** export (`airdraw_###.png`)  
✅ Hand landmarks overlay & detection status  
✅ Mirror toggle (selfie view)  
✅ Fast, offline — Python + OpenCV + MediaPipe

---

## 🔗 Demo

- 🎥 **Time-lapse / demo video:** (https://www.facebook.com/share/v/178SufaSA1/)*  
- 📦 **Repo code:** this repository

---

## 🖥️ Tech Stack

- 🐍 Python (3.9–3.11 recommended)  
- 🧠 MediaPipe Hands  
- 🎥 OpenCV  
- 🔢 NumPy

---

## ⚙️ Setup

**1) Clone or Download**
```bash
git clone https://github.com/<your-username>/airdraw-python.git
cd airdraw-python
```
Or download ZIP → extract → open folder in a terminal.

**2) Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3) Install dependencies**
```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, create one with:
> ```
> opencv-python
> mediapipe
> numpy
> ```

---

## ▶️ Run

```bash
python airdraw.py
```

- A preview window opens — allow camera access if prompted.  
- Keep your hand ~30–60 cm from the camera with good lighting.  
- **Pinch** thumb + index to draw. Unpinch to move without drawing.

---

## 🎛️ Controls

| Action                     | Key(s)                    |
|---------------------------|---------------------------|
| Draw (pinch)              | Thumb + index pinch       |
| Brush size                | `+` / `-`                 |
| Change color              | Click swatch or `1–8`     |
| Undo                      | `Z` or `U`                |
| Redo                      | `Y` or `R`                |
| Clear canvas              | `C`                       |
| Save **transparent PNG**  | `S`                       |
| Mirror on/off             | `M`                       |
| Quit                      | `Q`                       |

---

## 🧠 How it Works (Quick)

- **MediaPipe Hands** tracks 21 landmarks in real time.  
- Distance between **thumb tip (4)** and **index tip (8)** indicates a *pinch*.  
- The index tip drives a smoothed cursor; when pinching, strokes are drawn onto an **RGBA canvas** (preserves transparency).  
- The canvas is alpha-blended over the camera preview for the UI.  
- Undo/Redo stores lightweight canvas snapshots.

Adjustable constants in `airdraw.py`:
```python
CAM_INDEX = 0            # 1 for external webcam
FRAME_W, FRAME_H = 1280, 720
PINCH_THRESHOLD = 0.060  # lower = pinch tighter
SMOOTH_ALPHA = 0.45      # higher = smoother, a bit laggier
MIRROR = True
```

---

## 🧪 Troubleshooting

- **Left/right feels reversed** → press **M** (mirror toggle).  
- **Black window / no camera** → set `CAM_INDEX = 1` for external webcam; close other camera apps.  
- **Hand not detected** → improve lighting; keep hand within frame & ~30–60 cm away.  
- **Install errors (mediapipe)** → use Python 3.9–3.11 in a fresh venv.  
- **PNG not transparent** → view the saved `airdraw_###.png` in software that supports alpha.

---

## 🧰 One-Click App (optional)

**Windows**
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name AirDraw airdraw.py
# Output: dist/AirDraw.exe
```

**macOS**
```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name AirDraw airdraw.py
# Output: dist/AirDraw
```
*(On macOS you may need: right-click → Open.)*

---

## 📂 Project Structure

```
airdraw-python/
├─ airdraw.py              # main app
├─ requirements.txt        # opencv-python, mediapipe, numpy
├─ README.md               # this file
└─ airdraw_###.png         # saved drawings appear here
```

---

## 🧑‍💻 Developed By

**Md. Naimur Rahman Jisan**  
🎓 Department of CSE | 🏫 State University of Bangladesh (SUB)  
📍 Bangladesh

---

## 📬 Let’s Connect!

<p align="center">
  <a href="https://www.linkedin.com/in/naimur-rahman-jisan/" target="_blank">
    <img src="https://user-images.githubusercontent.com/74038190/235294012-0a55e343-37ad-4b0f-924f-c8431d9d2483.gif" width="100" alt="LinkedIn"/>
  </a>&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.instagram.com/naimurrahmanjisan99/" target="_blank">
    <img src="https://user-images.githubusercontent.com/74038190/235294013-a33e5c43-a01c-43f6-b44d-a406d8b4ab75.gif" width="100" alt="Instagram"/>
  </a>&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.facebook.com/nrjisan" target="_blank">
    <img src="https://user-images.githubusercontent.com/74038190/235294010-ec412ef5-e3da-4efa-b1d4-0ab4d4638755.gif" width="100" alt="Facebook"/>
  </a>
</p>

---

## ⭐ If You Like This Repo

Give it a **star ⭐** and share it with friends who love Computer Vision & Python!

<p align="center">
  <img src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif" width="300" alt="thank you gif"/>
</p>

---

## 📜 License

This project is open-source under the **MIT License**.

---

<p align="center">
  <img src="https://readme-typing-svg.demolab.com/?lines=Thanks+for+visiting!;Made+as+fun+project!;See+You+Soon!&center=true&width=500&height=30&color=58A6FF&vCenter=true&size=20"/> 
  <br/>
  Built with 💙 by <a href="https://github.com/nr-jisan">Naimur Rahman Jisan</a>
</p>
