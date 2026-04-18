import tkinter as tk
from tkinter import font as tkfont
import random

# ── Palette ───────────────────────────────────────────────────────────────────
BG         = "#0a3d1f"   # deep casino green
FELT       = "#0d4a26"
RAIL       = "#7c3f00"
GOLD       = "#f0c040"
GOLD2      = "#c8960a"
TEXT       = "#f5f0e8"
MUTED      = "#a09080"
RED_C      = "#d42b2b"
BLACK_C    = "#1a1a1a"
CARD_BG    = "#fdfaf4"
CARD_BORDER = "#c8b89a"
BTN_HIT    = "#1a6b35"
BTN_STAND  = "#8b2020"
BTN_NEW    = "#7c3f00"
WIN_CLR    = "#f0c040"
LOSE_CLR   = "#e05050"
TIE_CLR    = "#a0c0ff"

SUITS = {"♠": BLACK_C, "♣": BLACK_C, "♥": RED_C, "♦": RED_C}
SUIT_LIST = ["♠", "♣", "♥", "♦"]
RANKS = {11: "A", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6",
         7: "7", 8: "8", 9: "9", 10: "10"}
DECK_VALUES = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

root = tk.Tk()
root.title("Blackjack")
root.geometry("700x620")
root.resizable(False, False)
root.configure(bg=BG)

TITLE_F = tkfont.Font(family="Georgia", size=22, weight="bold")
CARD_NUM_F = tkfont.Font(family="Georgia", size=18, weight="bold")
CARD_SUIT_F = tkfont.Font(family="Georgia", size=22)
CARD_CORNER_F = tkfont.Font(family="Georgia", size=11, weight="bold")
LABEL_F = tkfont.Font(family="Georgia", size=12)
SCORE_F = tkfont.Font(family="Georgia", size=13, weight="bold")
BTN_F   = tkfont.Font(family="Georgia", size=13, weight="bold")
STATUS_F= tkfont.Font(family="Georgia", size=18, weight="bold")

# ── Game state ────────────────────────────────────────────────────────────────
state = {
    "player": [], "dealer": [], "game_over": False,
    "wins": 0, "losses": 0, "ties": 0
}

def adjust_ace(hand):
    """Convert Aces from 11 to 1 if the total exceeds 21."""
    while sum(hand) > 21 and 11 in hand:
        hand[hand.index(11)] = 1
    return sum(hand)

def deal_card():
    return random.choice(DECK_VALUES)

def card_suit(idx):
    return SUIT_LIST[idx % 4]

# ── Card drawing on Canvas ────────────────────────────────────────────────────
CARD_W, CARD_H = 72, 100
CARD_GAP = 12

def draw_card(canvas, x, y, value, suit, face_down=False):
    # Shadow
    canvas.create_rectangle(x+3, y+3, x+CARD_W+3, y+CARD_H+3,
                            fill="#000000", outline="", tags="card", stipple="gray25")
    # Card body
    canvas.create_rectangle(x, y, x+CARD_W, y+CARD_H,
                            fill="#1a4a30" if face_down else CARD_BG,
                            outline=CARD_BORDER, width=1.5, tags="card")

    if face_down:
        # Decorative back pattern
        for i in range(4, CARD_H-4, 8):
            canvas.create_line(x+4, y+i, x+CARD_W-4, y+i,
                               fill="#0d3a22", width=1, tags="card")
        canvas.create_text(x+CARD_W//2, y+CARD_H//2,
                           text="?", font=CARD_NUM_F,
                           fill=GOLD, tags="card")
        return x + CARD_W

    rank = RANKS.get(value, str(value))
    color = SUITS.get(suit, BLACK_C)

    # Corners and Center
    canvas.create_text(x+8, y+10, text=rank, font=CARD_CORNER_F, fill=color, anchor="nw", tags="card")
    canvas.create_text(x+CARD_W-8, y+CARD_H-10, text=rank, font=CARD_CORNER_F, fill=color, anchor="se", tags="card")
    canvas.create_text(x+CARD_W//2, y+CARD_H//2, text=suit, font=CARD_SUIT_F, fill=color, tags="card")

    return x + CARD_W

def draw_hand(canvas, hand, y, hide_second=False):
    canvas.delete("card")
    total = len(hand)
    total_w = total * CARD_W + (total - 1) * CARD_GAP
    canvas_w = 680
    start_x = (canvas_w - total_w) // 2

    for i, value in enumerate(hand):
        suit = SUIT_LIST[i % 4] 
        face_down = (hide_second and i == 1)
        draw_card(canvas, start_x + i * (CARD_W + CARD_GAP), y, value, suit, face_down)

# ── UI Layout ─────────────────────────────────────────────────────────────────
title_bar = tk.Frame(root, bg=RAIL, height=48)
title_bar.pack(fill="x")
tk.Label(title_bar, text="♠  BLACKJACK  ♠", bg=RAIL, fg=GOLD, font=TITLE_F).pack(side="left", padx=20)

stats_frame = tk.Frame(title_bar, bg=RAIL)
stats_frame.pack(side="right", padx=20)
wins_var, losses_var, ties_var = tk.StringVar(value="W: 0"), tk.StringVar(value="L: 0"), tk.StringVar(value="T: 0")
for var, clr in [(wins_var, "#80ff80"), (losses_var, "#ff8080"), (ties_var, TIE_CLR)]:
    tk.Label(stats_frame, textvariable=var, bg=RAIL, fg=clr, font=LABEL_F).pack(side="left", padx=6)

felt = tk.Frame(root, bg=FELT)
felt.pack(fill="both", expand=True)

# Dealer
tk.Label(felt, text="DEALER", bg=FELT, fg=GOLD2, font=LABEL_F).pack(pady=(10,0))
dealer_score_var = tk.StringVar()
tk.Label(felt, textvariable=dealer_score_var, bg=FELT, fg=TEXT, font=SCORE_F).pack()
dealer_canvas = tk.Canvas(felt, bg=FELT, height=CARD_H+20, highlightthickness=0, width=680)
dealer_canvas.pack()

# Status
status_var = tk.StringVar()
status_lbl = tk.Label(felt, textvariable=status_var, bg=FELT, fg=GOLD, font=STATUS_F)
status_lbl.pack(pady=5)

# Player
player_canvas = tk.Canvas(felt, bg=FELT, height=CARD_H+20, highlightthickness=0, width=680)
player_canvas.pack()
player_score_var = tk.StringVar()
tk.Label(felt, textvariable=player_score_var, bg=FELT, fg=TEXT, font=SCORE_F).pack()
tk.Label(felt, text="YOUR HAND", bg=FELT, fg=GOLD2, font=LABEL_F).pack()

# Buttons
btn_row = tk.Frame(felt, bg=FELT)
btn_row.pack(pady=20)

def make_btn(text, cmd, color):
    return tk.Button(btn_row, text=text, command=cmd, bg=color, fg=TEXT, font=BTN_F, 
                     relief="flat", width=10, cursor="hand2")

hit_btn = make_btn("HIT", lambda: player_hit(), BTN_HIT)
stand_btn = make_btn("STAND", lambda: player_stand(), BTN_STAND)
new_btn = make_btn("NEW GAME", lambda: new_game(), BTN_NEW)
for b in [hit_btn, stand_btn, new_btn]: b.pack(side="left", padx=10)

# ── Game logic ────────────────────────────────────────────────────────────────
def render(hide_dealer=True):
    draw_hand(dealer_canvas, state["dealer"], 10, hide_second=hide_dealer)
    draw_hand(player_canvas, state["player"], 10)
    
    p_sum = sum(state["player"])
    player_score_var.set(f"Score: {p_sum}")
    
    if hide_dealer:
        dealer_score_var.set(f"Showing: {state['dealer'][0]}")
    else:
        d_sum = sum(state["dealer"])
        dealer_score_var.set(f"Score: {d_sum}")

def new_game():
    state["player"] = [deal_card(), deal_card()]
    state["dealer"] = [deal_card(), deal_card()]
    state["game_over"] = False
    adjust_ace(state["player"])
    adjust_ace(state["dealer"])
    
    status_var.set("")
    hit_btn.config(state="normal", bg=BTN_HIT)
    stand_btn.config(state="normal", bg=BTN_STAND)
    render(hide_dealer=True)
    
    if sum(state["player"]) == 21:
        player_stand()

def player_hit():
    if state["game_over"]: return
    state["player"].append(deal_card())
    if adjust_ace(state["player"]) > 21:
        end_game("bust")
    render(hide_dealer=True)

def player_stand():
    if state["game_over"]: return
    
    # Dealer plays now
    while sum(state["dealer"]) < 17:
        state["dealer"].append(deal_card())
        adjust_ace(state["dealer"])
        
    p, d = sum(state["player"]), sum(state["dealer"])
    if d > 21: end_game("dealer_bust")
    elif p > d: end_game("win")
    elif p < d: end_game("lose")
    else: end_game("tie")

def end_game(result):
    state["game_over"] = True
    hit_btn.config(state="disabled", bg="#333")
    stand_btn.config(state="disabled", bg="#333")
    
    results = {
        "bust": ("💥 Bust! You lose.", LOSE_CLR, "losses"),
        "dealer_bust": ("🎉 Dealer busted! Win!", WIN_CLR, "wins"),
        "win": ("✨ You win!", WIN_CLR, "wins"),
        "lose": ("😔 You lose.", LOSE_CLR, "losses"),
        "tie": ("🤝 It's a tie.", TIE_CLR, "ties")
    }
    
    msg, clr, stat = results[result]
    status_var.set(msg)
    status_lbl.config(fg=clr)
    state[stat] += 1
    
    wins_var.set(f"W: {state['wins']}")
    losses_var.set(f"L: {state['losses']}")
    ties_var.set(f"T: {state['ties']}")
    render(hide_dealer=False)

new_game()
root.mainloop()