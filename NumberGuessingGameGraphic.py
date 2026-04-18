import tkinter as tk
from tkinter import font as tkfont
import random

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#1a1a2e"
CARD      = "#16213e"
ACCENT    = "#e94560"
ACCENT2   = "#0f3460"
TEXT      = "#eaeaea"
MUTED     = "#8888aa"
SUCCESS   = "#4ecca3"
WARNING   = "#f5a623"
BTN_FG    = "#ffffff"
ENTRY_BG  = "#0d0d1a"

# ── Root window ───────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("480x620")
root.resizable(False, False)
root.configure(bg=BG)

TITLE_FONT  = tkfont.Font(family="Helvetica", size=22, weight="bold")
BODY_FONT   = tkfont.Font(family="Helvetica", size=13)
SMALL_FONT  = tkfont.Font(family="Helvetica", size=11)
BTN_FONT    = tkfont.Font(family="Helvetica", size=13, weight="bold")
LABEL_FONT  = tkfont.Font(family="Helvetica", size=12)

# ── Helper: clear root and build fresh frames ─────────────────────────────────
def clear():
    for w in root.winfo_children():
        w.destroy()

def card_frame(parent, **kw):
    return tk.Frame(parent, bg=CARD, **kw)

def btn(parent, text, cmd, color=ACCENT, width=18):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=color, fg=BTN_FG, font=BTN_FONT,
                  relief="flat", bd=0, cursor="hand2",
                  padx=12, pady=8, width=width,
                  activebackground=ACCENT2, activeforeground=BTN_FG)
    return b

def label(parent, text, color=TEXT, size=13, bold=False):
    wt = "bold" if bold else "normal"
    f  = tkfont.Font(family="Helvetica", size=size, weight=wt)
    return tk.Label(parent, text=text, bg=parent["bg"], fg=color, font=f, wraplength=400)

def entry(parent):
    e = tk.Entry(parent, font=BODY_FONT, bg=ENTRY_BG, fg=TEXT,
                 insertbackground=TEXT, relief="flat",
                 justify="center", width=10)
    e.configure(highlightthickness=2, highlightcolor=ACCENT,
                highlightbackground=MUTED)
    return e

# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN 1 – Mode Select
# ═══════════════════════════════════════════════════════════════════════════════
def screen_mode():
    clear()
    tk.Label(root, text="🎯", bg=BG, fg=TEXT,
             font=tkfont.Font(size=48)).pack(pady=(50, 8))
    label(root, "Number Guessing Game", bold=True, size=24).pack()
    label(root, "Choose your mode", color=MUTED, size=13).pack(pady=(4, 30))

    f = card_frame(root, padx=30, pady=30)
    f.pack(padx=40, fill="x")

    btn(f, "🧍  Singleplayer", screen_difficulty).pack(pady=8, fill="x")
    btn(f, "👥  Multiplayer",  screen_mp_input, color=ACCENT2).pack(pady=8, fill="x")

    label(root, "Guess the secret number between 1 and 100",
          color=MUTED, size=11).pack(side="bottom", pady=16)

# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN 2 – Difficulty
# ═══════════════════════════════════════════════════════════════════════════════
def screen_difficulty():
    clear()
    label(root, "Select Difficulty", bold=True, size=20).pack(pady=(50, 8))
    label(root, "How many guesses do you get?", color=MUTED).pack(pady=(0, 30))

    f = card_frame(root, padx=30, pady=30)
    f.pack(padx=40, fill="x")

    label(f, "🟢  Easy  —  10 guesses", size=13).pack(pady=6)
    btn(f, "Play Easy",  lambda: screen_sp_game(10), color=SUCCESS).pack(pady=4, fill="x")

    tk.Frame(f, bg=MUTED, height=1).pack(fill="x", pady=12)

    label(f, "🔴  Hard  —  5 guesses", size=13).pack(pady=6)
    btn(f, "Play Hard", lambda: screen_sp_game(5),  color=ACCENT).pack(pady=4, fill="x")

    btn(root, "← Back", screen_mode, color=ACCENT2, width=10).pack(pady=20)

# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN 3 – Singleplayer Game
# ═══════════════════════════════════════════════════════════════════════════════
def screen_sp_game(max_guesses):
    number = random.randint(1, 100)
    guesses_left = [max_guesses]

    clear()
    root.configure(bg=BG)

    # Header
    label(root, "Singleplayer", bold=True, size=20).pack(pady=(30, 0))
    label(root, "I'm thinking of a number between 1 and 100", color=MUTED).pack(pady=4)

    # Guess counter
    counter_var = tk.StringVar(value=f"Guesses remaining: {max_guesses}")
    counter_lbl = tk.Label(root, textvariable=counter_var,
                           bg=BG, fg=WARNING,
                           font=tkfont.Font(family="Helvetica", size=13, weight="bold"))
    counter_lbl.pack(pady=6)

    # Card
    f = card_frame(root, padx=30, pady=24)
    f.pack(padx=40, fill="x")

    label(f, "Enter your guess:", size=12, color=MUTED).pack()
    guess_entry = entry(f)
    guess_entry.pack(pady=10, ipady=8, fill="x")
    guess_entry.focus()

    feedback_var = tk.StringVar(value="")
    feedback_lbl = tk.Label(f, textvariable=feedback_var,
                            bg=CARD, fg=TEXT,
                            font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                            wraplength=380)
    feedback_lbl.pack(pady=8)

    def submit(event=None):
        raw = guess_entry.get().strip()
        if not raw.lstrip("-").isdigit():
            feedback_var.set("⚠️  Enter a whole number!")
            feedback_lbl.config(fg=WARNING)
            return

        g = int(raw)
        guess_entry.delete(0, tk.END)
        guesses_left[0] -= 1
        counter_var.set(f"Guesses remaining: {guesses_left[0]}")

        if g == number:
            feedback_var.set(f"🎉 Correct! It was {number}!")
            feedback_lbl.config(fg=SUCCESS)
            guess_btn.config(state="disabled")
            guess_entry.config(state="disabled")
        elif guesses_left[0] == 0:
            feedback_var.set(f"💀 Out of guesses! It was {number}.")
            feedback_lbl.config(fg=ACCENT)
            guess_btn.config(state="disabled")
            guess_entry.config(state="disabled")
        elif g > number:
            feedback_var.set(f"📉 Too high!")
            feedback_lbl.config(fg=ACCENT)
        else:
            feedback_var.set(f"📈 Too low!")
            feedback_lbl.config(fg=ACCENT2)

    root.bind("<Return>", submit)

    guess_btn = btn(f, "Guess!", submit)
    guess_btn.pack(fill="x", pady=4)

    btn(root, "🔁 Play Again", lambda: screen_difficulty(), color=ACCENT2, width=14).pack(pady=8)
    btn(root, "← Menu",        screen_mode,                 color=ACCENT2, width=14).pack()

# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN 4 – Multiplayer: secret number entry
# ═══════════════════════════════════════════════════════════════════════════════
def screen_mp_input():
    player = [1]
    numbers = [None, None]

    clear()
    label(root, "Multiplayer Setup", bold=True, size=20).pack(pady=(40, 4))

    info_var  = tk.StringVar(value="Player 1: enter your secret number")
    sub_var   = tk.StringVar(value="(Player 2, look away!)")
    info_lbl  = tk.Label(root, textvariable=info_var,  bg=BG, fg=TEXT,
                         font=BTN_FONT)
    sub_lbl   = tk.Label(root, textvariable=sub_var,   bg=BG, fg=MUTED,
                         font=SMALL_FONT)
    info_lbl.pack()
    sub_lbl.pack(pady=(2, 20))

    f = card_frame(root, padx=30, pady=24)
    f.pack(padx=40, fill="x")

    label(f, "Secret number (1–100):", color=MUTED, size=12).pack()
    sec_entry = entry(f)
    sec_entry.pack(pady=10, ipady=8, fill="x")
    sec_entry.focus()

    err_var = tk.StringVar()
    tk.Label(f, textvariable=err_var, bg=CARD, fg=ACCENT,
             font=SMALL_FONT).pack()

    def confirm(event=None):
        raw = sec_entry.get().strip()
        if not raw.isdigit() or not (1 <= int(raw) <= 100):
            err_var.set("Enter a number between 1 and 100")
            return
        numbers[player[0] - 1] = int(raw)
        sec_entry.delete(0, tk.END)
        err_var.set("")

        if player[0] == 1:
            player[0] = 2
            info_var.set("Player 2: enter your secret number")
            sub_var.set("(Player 1, look away!)")
            confirm_btn.config(text="Confirm →")
        else:
            screen_mp_game(numbers[0], numbers[1])

    root.bind("<Return>", confirm)

    confirm_btn = btn(f, "Confirm →", confirm)
    confirm_btn.pack(fill="x", pady=4)

    btn(root, "← Back", screen_mode, color=ACCENT2, width=10).pack(pady=16)

# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN 5 – Multiplayer Game
# ═══════════════════════════════════════════════════════════════════════════════
def screen_mp_game(num1, num2):
    # State
    turn          = [1]
    guessed       = [False, False]   # [p2_cracked, p1_cracked]
    turn_count    = [1]

    clear()

    # Header
    header_var = tk.StringVar(value="Turn 1  ·  Player 1's guess")
    tk.Label(root, textvariable=header_var, bg=BG, fg=TEXT,
             font=TITLE_FONT).pack(pady=(28, 4))

    # Score bar
    score_frame = tk.Frame(root, bg=BG)
    score_frame.pack(pady=4)

    p1_var = tk.StringVar(value="Player 1  ❌")
    p2_var = tk.StringVar(value="Player 2  ❌")
    p1_score = tk.Label(score_frame, textvariable=p1_var, bg=ACCENT2, fg=TEXT,
                        font=LABEL_FONT, padx=14, pady=6)
    p1_score.pack(side="left", padx=6)
    p2_score = tk.Label(score_frame, textvariable=p2_var, bg=ACCENT2, fg=TEXT,
                        font=LABEL_FONT, padx=14, pady=6)
    p2_score.pack(side="left", padx=6)

    task_var = tk.StringVar(value="Guess Player 2's number:")
    tk.Label(root, textvariable=task_var, bg=BG, fg=MUTED,
             font=LABEL_FONT).pack(pady=(14, 2))

    f = card_frame(root, padx=30, pady=20)
    f.pack(padx=40, fill="x")

    guess_e = entry(f)
    guess_e.pack(pady=8, ipady=8, fill="x")
    guess_e.focus()

    feedback_var = tk.StringVar()
    feedback_lbl = tk.Label(f, textvariable=feedback_var,
                            bg=CARD, fg=TEXT,
                            font=tkfont.Font(family="Helvetica", size=14, weight="bold"),
                            wraplength=380)
    feedback_lbl.pack(pady=6)

    def update_header():
        p = turn[0]
        target = 2 if p == 1 else 1
        header_var.set(f"Turn {turn_count[0]}  ·  Player {p}'s guess")
        task_var.set(f"Guess Player {target}'s number:")

    def mark_winner(p):
        if p == 1:
            p1_var.set("Player 1  ✅")
            p1_score.config(bg=SUCCESS, fg="#0d1a13")
        else:
            p2_var.set("Player 2  ✅")
            p2_score.config(bg=SUCCESS, fg="#0d1a13")

    def submit(event=None):
        raw = guess_e.get().strip()
        if not raw.lstrip("-").isdigit():
            feedback_var.set("⚠️  Enter a whole number!")
            feedback_lbl.config(fg=WARNING)
            return

        g = int(raw)
        guess_e.delete(0, tk.END)
        p = turn[0]
        # guessed[0] = P1 cracked P2's number
        # guessed[1] = P2 cracked P1's number
        secret = num2 if p == 1 else num1
        idx    = 0 if p == 1 else 1

        just_won = False
        if g == secret:
            guessed[idx] = True
            just_won = True
            mark_winner(p)
            feedback_var.set(f"🎉 Player {p} cracked it! It was {secret}!")
            feedback_lbl.config(fg=SUCCESS)
        elif g > secret:
            feedback_var.set(f"📉 Too high!")
            feedback_lbl.config(fg=ACCENT)
        else:
            feedback_var.set(f"📈 Too low!")
            feedback_lbl.config(fg=ACCENT2)

        def end_game(winner):
            guess_btn.config(state="disabled")
            guess_e.config(state="disabled")
            root.after(1200, lambda: screen_result(winner, num1, num2))

        # P1 just guessed correctly — P2 gets one last shot this same turn
        if just_won and p == 1 and not guessed[1]:
            turn[0] = 2
            feedback_var.set(f"🎉 P1 got it! P2 gets one last chance...")
            update_header()
            return

        # P2 just finished their half-turn — evaluate end of full turn
        if p == 2:
            if guessed[0] and guessed[1]:
                feedback_var.set(f"🤝 Both cracked it on turn {turn_count[0]}! It's a tie!")
                feedback_lbl.config(fg=WARNING)
                guess_btn.config(state="disabled")
                guess_e.config(state="disabled")
                return
            elif guessed[0]:        # only P1 had cracked it
                end_game("Player 1")
                return
            elif guessed[1]:        # only P2 just cracked it
                end_game("Player 2")
                return
            # nobody won yet — start next full turn
            turn_count[0] += 1
            turn[0] = 1
            update_header()
            return

        # P1 didn't win — pass to P2
        turn[0] = 2
        update_header()

    root.bind("<Return>", submit)

    guess_btn = btn(f, "Guess!", submit)
    guess_btn.pack(fill="x", pady=4)

    btn(root, "← Menu", screen_mode, color=ACCENT2, width=10).pack(pady=12)

# ═══════════════════════════════════════════════════════════════════════════════
#  SCREEN 6 – Result
# ═══════════════════════════════════════════════════════════════════════════════
def screen_result(winner, num1, num2):
    clear()
    tk.Label(root, text="🏆", bg=BG, fg=TEXT,
             font=tkfont.Font(size=64)).pack(pady=(60, 8))
    label(root, f"{winner} Wins!", bold=True, size=26, color=SUCCESS).pack()
    label(root, f"The numbers were  {num1}  and  {num2}", color=MUTED, size=13).pack(pady=10)

    f = card_frame(root, padx=30, pady=24)
    f.pack(padx=40, fill="x", pady=30)

    btn(f, "🔁 Play Again", screen_mp_input, width=20).pack(fill="x", pady=6)
    btn(f, "← Main Menu",  screen_mode,     color=ACCENT2, width=20).pack(fill="x")

# ── Launch ────────────────────────────────────────────────────────────────────
screen_mode()
root.mainloop()