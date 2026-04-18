import tkinter as tk
from tkinter import font as tkfont
import math

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = "#1c1c2e"
SURFACE   = "#2a2a48"
WORK_CLR  = "#e05c7a"
BREAK_CLR = "#52c7a8"
TEXT      = "#f0eeff"
MUTED     = "#6a6a8a"
BTN_BG    = "#2e2e50"
BTN_HOV   = "#3a3a60"

WORK_MIN   = 25
SHORT_MIN  = 5
LONG_MIN   = 15
LONG_EVERY = 4

# ── Root ──────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Pomodoro Timer")
root.geometry("420x560")
root.resizable(False, False)
root.configure(bg=BG)

DISPLAY_F = tkfont.Font(family="Courier", size=46, weight="bold")
MODE_F    = tkfont.Font(family="Courier", size=13, weight="bold")
BTN_F     = tkfont.Font(family="Courier", size=12, weight="bold")
SMALL_F   = tkfont.Font(family="Courier", size=10)
DOT_F     = tkfont.Font(family="Courier", size=15)

# ── State ─────────────────────────────────────────────────────────────────────
state = {
    "running":       False,
    "mode":          "work",
    "seconds_left":  WORK_MIN * 60,
    "total_seconds": WORK_MIN * 60,
    "pomodoros":     0,
    "after_id":      None,
}

def mode_color():
    return WORK_CLR if state["mode"] == "work" else BREAK_CLR

def mode_label():
    return {"work": "FOCUS", "short": "SHORT BREAK", "long": "LONG BREAK"}[state["mode"]]

def mode_seconds():
    return {"work": WORK_MIN, "short": SHORT_MIN, "long": LONG_MIN}[state["mode"]] * 60

# ── Canvas ────────────────────────────────────────────────────────────────────
CX, CY, R, RW = 210, 190, 130, 16

canvas = tk.Canvas(root, width=420, height=380, bg=BG, highlightthickness=0)
canvas.pack()

def draw_ring():
    canvas.delete("all")
    frac  = max(0, state["seconds_left"] / state["total_seconds"])
    color = mode_color()

    # Outer glow ring (subtle)
    canvas.create_oval(CX-R-4, CY-R-4, CX+R+4, CY+R+4,
                       outline=color, width=1, stipple="gray25")

    # Background track
    canvas.create_oval(CX-R, CY-R, CX+R, CY+R,
                       outline=SURFACE, width=RW)

    # Progress arc — tkinter arc: start=90 = top, extent goes CCW
    if frac > 0.001:
        extent = frac * 359.99  # avoid full-circle bug
        canvas.create_arc(CX-R, CY-R, CX+R, CY+R,
                          start=90, extent=extent,
                          outline=color, width=RW, style="arc")

        # Dot at the leading edge of the arc
        angle_deg = 90 + extent
        angle_rad = math.radians(angle_deg)
        tip_x = CX + R * math.cos(angle_rad)
        tip_y = CY - R * math.sin(angle_rad)
        canvas.create_oval(tip_x-9, tip_y-9, tip_x+9, tip_y+9,
                           fill=color, outline=BG, width=2)

    # Time display
    mins = state["seconds_left"] // 60
    secs = state["seconds_left"] % 60
    canvas.create_text(CX, CY - 18, text=f"{mins:02d}:{secs:02d}",
                       font=DISPLAY_F, fill=TEXT)

    # Mode label
    canvas.create_text(CX, CY + 34, text=mode_label(),
                       font=MODE_F, fill=color)

# ── Pomodoro dots ─────────────────────────────────────────────────────────────
dots_frame = tk.Frame(root, bg=BG)
dots_frame.pack(pady=(0, 4))
dot_labels = []
for i in range(LONG_EVERY):
    d = tk.Label(dots_frame, text="●", bg=BG, fg=MUTED, font=DOT_F)
    d.pack(side="left", padx=5)
    dot_labels.append(d)

session_var = tk.StringVar(value="0 pomodoros completed")
tk.Label(root, textvariable=session_var, bg=BG, fg=MUTED, font=SMALL_F).pack()

def update_dots():
    filled = state["pomodoros"] % LONG_EVERY
    for i, d in enumerate(dot_labels):
        d.config(fg=WORK_CLR if i < filled else MUTED)
    p = state["pomodoros"]
    session_var.set(f"{p} pomodoro{'s' if p != 1 else ''} completed")

# ── Buttons ───────────────────────────────────────────────────────────────────
btn_row = tk.Frame(root, bg=BG)
btn_row.pack(pady=12)

def make_btn(parent, text, cmd, width=9):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=BTN_BG, fg=TEXT, font=BTN_F,
                  relief="flat", bd=0, cursor="hand2",
                  padx=12, pady=9, width=width,
                  activebackground=BTN_HOV, activeforeground=TEXT)
    b.pack(side="left", padx=5)
    return b

# ── Logic (defined before buttons so lambdas can reference) ───────────────────
def tick():
    if not state["running"]:
        return
    if state["seconds_left"] > 0:
        state["seconds_left"] -= 1
        draw_ring()
        state["after_id"] = root.after(1000, tick)
    else:
        timer_done()

def timer_done():
    state["running"] = False
    start_btn.config(text="▶  START")
    root.bell()   # system beep — works on all platforms

    if state["mode"] == "work":
        state["pomodoros"] += 1
        update_dots()
        next_mode = "long" if state["pomodoros"] % LONG_EVERY == 0 else "short"
        set_mode(next_mode, auto=True)
    else:
        set_mode("work", auto=True)

def toggle():
    if state["running"]:
        state["running"] = False
        if state["after_id"]:
            root.after_cancel(state["after_id"])
        start_btn.config(text="▶  START")
    else:
        state["running"] = True
        start_btn.config(text="⏸  PAUSE")
        tick()

def reset():
    state["running"] = False
    if state["after_id"]:
        root.after_cancel(state["after_id"])
    state["seconds_left"] = mode_seconds()
    state["total_seconds"] = mode_seconds()
    start_btn.config(text="▶  START")
    draw_ring()

def set_mode(mode, auto=False):
    state["running"] = False
    if state["after_id"]:
        root.after_cancel(state["after_id"])
    state["mode"]          = mode
    state["seconds_left"]  = mode_seconds()
    state["total_seconds"] = mode_seconds()
    start_btn.config(text="▶  START")
    draw_ring()
    update_dots()
    if auto:
        toggle()

start_btn = make_btn(btn_row, "▶  START", toggle)
reset_btn = make_btn(btn_row, "↺  RESET", reset)

# Mode jump row
mode_row = tk.Frame(root, bg=BG)
mode_row.pack()
tk.Label(mode_row, text="Jump to:", bg=BG, fg=MUTED, font=SMALL_F).pack(side="left", padx=4)
make_btn(mode_row, "Focus",   lambda: set_mode("work"),  width=7)
make_btn(mode_row, "Short ☕", lambda: set_mode("short"), width=8)
make_btn(mode_row, "Long 🌿",  lambda: set_mode("long"),  width=8)

# Settings tip
tk.Label(root,
         text=f"Focus {WORK_MIN}m  ·  Short {SHORT_MIN}m  ·  Long {LONG_MIN}m every {LONG_EVERY} sessions",
         bg=BG, fg=MUTED, font=SMALL_F).pack(side="bottom", pady=10)

# Spacebar shortcut
root.bind("<space>", lambda e: toggle())

# ── Init ──────────────────────────────────────────────────────────────────────
draw_ring()
update_dots()
root.mainloop()