import tkinter as tk
import subprocess
import os
import sys



APP_NAME = "FatalCraft"
WIDTH, HEIGHT = 900, 550

BG = "#0f0f0f"
PANEL = "#1a1a1a"
BTN = "#242424"
BTN_HOVER = "#3a3a3a"
ACCENT = "#ff3b3b"
TEXT = "#eaeaea"


root = tk.Tk()
root.title(APP_NAME)
root.geometry(f"{WIDTH}x{HEIGHT}")
root.resizable(False, False)
root.configure(bg=BG)

canvas = tk.Canvas(
    root,
    width=WIDTH,
    height=HEIGHT,
    bg=BG,
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)


def start_game():
    try:
        if os.path.exists("main.exe"):
            subprocess.Popen(["main.exe"], shell=True)
        elif os.path.exists("main.py"):
            subprocess.Popen([sys.executable, "main.py"])
        else:
            show_status("Game file not found.")
            return
        root.destroy()
    except Exception as e:
        show_status(str(e))


buttons = []

def clear_canvas():
    canvas.delete("all")
    buttons.clear()

def show_status(msg):
    canvas.create_text(
        WIDTH // 2,
        HEIGHT - 30,
        text=msg,
        fill="#ff6b6b",
        font=("Arial", 11),
        tags="status"
    )

def draw_button(x, y, w, h, text, command):
    rect = canvas.create_rectangle(
        x - w//2, y - h//2,
        x + w//2, y + h//2,
        fill=BTN,
        outline=""
    )

    label = canvas.create_text(
        x, y,
        text=text,
        fill=TEXT,
        font=("Arial", 18)
    )

    def on_enter(_):
        canvas.itemconfig(rect, fill=BTN_HOVER)
        canvas.scale(rect, x, y, 1.05, 1.05)
        canvas.scale(label, x, y, 1.05, 1.05)

    def on_leave(_):
        canvas.itemconfig(rect, fill=BTN)
        canvas.scale(rect, x, y, 1/1.05, 1/1.05)
        canvas.scale(label, x, y, 1/1.05, 1/1.05)

    def on_click(_):
        command()

    for item in (rect, label):
        canvas.tag_bind(item, "<Enter>", on_enter)
        canvas.tag_bind(item, "<Leave>", on_leave)
        canvas.tag_bind(item, "<Button-1>", on_click)

    buttons.append((rect, label))



def show_main_menu():
    clear_canvas()

    # Title
    canvas.create_text(
        WIDTH // 2, 90,
        text="FATALCRAFT",
        fill=ACCENT,
        font=("Arial Black", 52)
    )

    canvas.create_text(
        WIDTH // 2, 145,
        text="ALPHA v1.1.2",
        fill=TEXT,
        font=("Arial", 14)
    )

    canvas.create_line(
        WIDTH//2 - 220, 175,
        WIDTH//2 + 220, 175,
        fill="#2a2a2a",
        width=2
    )

    draw_button(WIDTH//2, 260, 300, 64, "START GAME", start_game)
    draw_button(WIDTH//2, 340, 300, 64, "CONTROLS", show_controls)
    draw_button(WIDTH//2, 420, 300, 64, "EXIT", root.destroy)



def show_controls():
    clear_canvas()

    # Header
    canvas.create_text(
        WIDTH // 2, 75,
        text="CONTROLS",
        fill=ACCENT,
        font=("Arial Black", 38)
    )

    canvas.create_line(
        WIDTH//2 - 200, 110,
        WIDTH//2 + 200, 110,
        fill="#2a2a2a",
        width=2
    )


    panel_top = 135
    panel_bottom = 445   

    canvas.create_rectangle(
        WIDTH//2 - 300, panel_top,
        WIDTH//2 + 300, panel_bottom,
        fill=PANEL,
        outline="#2f2f2f",
        width=2
    )

    controls_text = (
        "Movement\n"
        "A / ←        Move Left\n"
        "D / →        Move Right\n"
        "W / Space    Jump\n"
        "Shift        Sprint\n\n"
        "Mouse\n"
        "Left Click   Mine / Attack\n"
        "Right Click  Place Block\n\n"
        "Inventory\n"
        "1 – 9        Hotbar Slots\n"
        "[ / ]        Cycle Slots\n"
        "E            Crafting\n"
        "ESC          Save & Quit"
    )

    canvas.create_text(
        WIDTH//2,
        (panel_top + panel_bottom)//2,
        text=controls_text,
        fill=TEXT,
        font=("Consolas", 13), 
        justify="left"
    )

    draw_button(
        WIDTH//2,
        HEIGHT - 60,  
        220,
        56,
        "BACK",
        show_main_menu
    )


show_main_menu()
root.mainloop()
