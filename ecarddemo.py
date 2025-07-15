import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import winsound

# Paths to card images
card_paths = {
    "Emperor": r"D:\projects\Emperor-Slave-card-game\emperor.jpg",
    "Citizen": r"D:\projects\Emperor-Slave-card-game\citizen.jpg",
    "Slave": r"D:\projects\Emperor-Slave-card-game\slave.jpg",
    "Back": r"D:\projects\Emperor-Slave-card-game\back.jpg"
}


class ECardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Card Game - Kaiji Style")
        # Store both PIL and Tk images for animation
        self.pil_images = {name: Image.open(path).resize((120, 180)) for name, path in card_paths.items()}
        self.card_images = {name: ImageTk.PhotoImage(self.pil_images[name]) for name in card_paths}
        self.player_score = 0
        self.cpu_score = 0
        self.show_role_selection()

    def show_role_selection(self):
        self.clear_screen()
        # Modern background frame
        bg_frame = tk.Frame(self.root, bg="#145a32")
        bg_frame.pack(fill="both", expand=True)

        # Modern gold-accented title
        title = tk.Label(bg_frame, text="Choose Your Role", font=("Arial", 28, "bold"), fg="#FFD700", bg="#145a32", pady=18)
        title.pack(pady=(40, 10))
        underline = tk.Frame(bg_frame, bg="#FFD700", height=3, width=320)
        underline.pack(pady=(0, 30))

        # Role selection buttons with images
        button_frame = tk.Frame(bg_frame, bg="#145a32")
        button_frame.pack(pady=10)

        # Emperor button
        emperor_img = self.card_images["Emperor"]
        emperor_btn = tk.Label(button_frame, image=emperor_img, text="Emperor", compound="top",
                              font=("Arial", 16, "bold"), fg="#FFD700", bg="#222", bd=6, relief="ridge",
                              padx=24, pady=18, cursor="hand2", highlightthickness=0)
        emperor_btn.grid(row=0, column=0, padx=40)
        emperor_btn.bind("<Enter>", lambda e: emperor_btn.config(bg="#333"))
        emperor_btn.bind("<Leave>", lambda e: emperor_btn.config(bg="#222"))
        emperor_btn.bind("<Button-1>", lambda e: (self.game.play_sound('click.wav') if hasattr(self, 'game') else None, self.start_game("Emperor", self.player_score, self.cpu_score)))

        # Slave button
        slave_img = self.card_images["Slave"]
        slave_btn = tk.Label(button_frame, image=slave_img, text="Slave", compound="top",
                            font=("Arial", 16, "bold"), fg="#FFD700", bg="#222", bd=6, relief="ridge",
                            padx=24, pady=18, cursor="hand2", highlightthickness=0)
        slave_btn.grid(row=0, column=1, padx=40)
        slave_btn.bind("<Enter>", lambda e: slave_btn.config(bg="#333"))
        slave_btn.bind("<Leave>", lambda e: slave_btn.config(bg="#222"))
        slave_btn.bind("<Button-1>", lambda e: (self.game.play_sound('click.wav') if hasattr(self, 'game') else None, self.start_game("Slave", self.player_score, self.cpu_score)))

    def start_game(self, role, player_score=0, cpu_score=0):
        self.clear_screen()
        self.game = ECardGame(self.root, self, role, self.card_images, player_score, cpu_score)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class ECardGame:
    def __init__(self, root, app, role, card_images, player_score=0, cpu_score=0):
        self.root = root
        self.role = role
        self.app = app
        self.cpu_role = "Slave" if role == "Emperor" else "Emperor"
        self.card_images = card_images
        self.pil_images = app.pil_images  # Access PIL images for animation

        self.player_hand = self.init_hand(self.role)
        self.cpu_hand = self.init_hand(self.cpu_role)

        self.chosen_player_card = None
        self.chosen_cpu_card = None
        self.history = []
        self.player_score = player_score
        self.cpu_score = cpu_score
        self.game_over = False

        # Main layout frames
        self.main_frame = tk.Frame(root, bg="#145a32", bd=4, relief="ridge")  # Green felt background
        self.main_frame.pack(side="left", padx=20, pady=20, ipadx=10, ipady=10)

        self.sidebar = tk.Frame(root)
        self.sidebar.pack(side="right", padx=10, fill="y")

        self.label = tk.Label(self.main_frame, text=f"You are playing as: {self.role}", font=("Arial", 14), bg="#145a32", fg="white")
        self.label.pack(pady=10)

        # Table layout
        self.table_frame = tk.Frame(self.main_frame, bg="#145a32")
        self.table_frame.pack(pady=30)

        # CPU played card (top center)
        self.cpu_card_slot = tk.Label(self.table_frame, image=self.card_images["Back"], bg="#145a32", bd=3, relief="groove")
        self.cpu_card_slot.grid(row=0, column=1, padx=30, pady=(0, 10))

        # VS label (large, prominent)
        self.vs_label = tk.Label(self.table_frame, text="VS", font=("Arial", 28, "bold"), bg="#145a32", fg="#FFD700")
        self.vs_label.grid(row=1, column=1, pady=10)

        # Player played card (bottom center)
        self.player_card_slot = tk.Label(self.table_frame, image=self.card_images["Back"], bg="#145a32", bd=3, relief="groove")
        self.player_card_slot.grid(row=2, column=1, padx=30, pady=(10, 0))

        self.result_label = tk.Label(self.main_frame, text="", font=("Arial", 12), bg="#145a32", fg="white")
        self.result_label.pack(pady=10)
        # Modern result banner
        self.result_banner = tk.Label(self.main_frame, text="", font=("Arial", 18, "bold"), bg="#222", fg="#fff", pady=10, padx=20)
        self.result_banner.pack(pady=(0, 10))

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.create_player_hand()  # New method for hand layout
        self.create_sidebar()

    def init_hand(self, role):
        if role == "Emperor":
            return ["Emperor"] + ["Citizen"] * 4
        else:
            return ["Slave"] + ["Citizen"] * 4

    def create_player_hand(self):
        # Remove old button_frame if it exists
        if hasattr(self, 'button_frame'):
            self.button_frame.destroy()
        self.hand_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.hand_frame.pack(pady=20)
        self.card_labels = []
        # Arrange cards in a row, allow duplicates
        for idx, card_name in enumerate(self.player_hand):
            lbl = tk.Label(
                self.hand_frame,
                image=self.card_images[card_name],
                bd=4,  # Always reserve max border
                relief="flat",
                bg="#2e2e2e",
                highlightthickness=2,  # Always reserve max highlight
                highlightbackground="#2e2e2e",
                highlightcolor="#2e2e2e"
            )
            lbl.grid(row=0, column=idx, padx=8)
            setattr(lbl, 'card_name', card_name)
            # Hover highlight (only change color/relief)
            lbl.bind("<Enter>", lambda e, l=lbl: l.config(relief="solid", highlightbackground="#FFD700", highlightcolor="#FFD700", bg="#393e46"))
            lbl.bind("<Leave>", lambda e, l=lbl: l.config(relief="flat", highlightbackground="#2e2e2e", highlightcolor="#2e2e2e", bg="#2e2e2e"))
            # Click to play
            lbl.bind("<Button-1>", lambda e, c=card_name: self.play_round(c))
            self.card_labels.append(lbl)

    def update_player_hand(self):
        # Refresh the hand display after a card is played
        for lbl in self.card_labels:
            lbl.destroy()
        self.card_labels = []
        for idx, card_name in enumerate(self.player_hand):
            lbl = tk.Label(
                self.hand_frame,
                image=self.card_images[card_name],
                bd=4,
                relief="flat",
                bg="#2e2e2e",
                highlightthickness=2,
                highlightbackground="#2e2e2e",
                highlightcolor="#2e2e2e"
            )
            lbl.grid(row=0, column=idx, padx=8)
            setattr(lbl, 'card_name', card_name)
            lbl.bind("<Enter>", lambda e, l=lbl: l.config(relief="solid", highlightbackground="#FFD700", highlightcolor="#FFD700", bg="#393e46"))
            lbl.bind("<Leave>", lambda e, l=lbl: l.config(relief="flat", highlightbackground="#2e2e2e", highlightcolor="#2e2e2e", bg="#2e2e2e"))
            lbl.bind("<Button-1>", lambda e, c=card_name: self.play_round(c))
            self.card_labels.append(lbl)

    def create_sidebar(self):
        # Scoreboard badge
        self.score_label = tk.Label(
            self.sidebar,
            text=self.get_score_text(),
            font=("Arial", 18, "bold"),
            fg="#333",
            bg="#FFD700",
            bd=2,
            relief="ridge",
            padx=18,
            pady=6,
            highlightthickness=0
        )
        self.score_label.pack(pady=(18, 18))

        # Button group frame
        btn_group = tk.Frame(self.sidebar, bg="#f5f5f5")
        btn_group.pack(pady=(0, 18), fill="x")
        btn_style = {"font": ("Arial", 11), "bg": "#fff", "fg": "#333", "activebackground": "#FFD700", "activeforeground": "#222", "relief": "groove", "bd": 2, "padx": 8, "pady": 4, "highlightthickness": 0}
        self.reset_score_btn = tk.Button(btn_group, text="Reset Score", command=lambda: (self.play_sound('click.wav'), self.reset_score()), **btn_style)
        self.reset_score_btn.pack(side="left", padx=4, pady=6)
        self.clear_history_btn = tk.Button(btn_group, text="Clear History", command=lambda: (self.play_sound('click.wav'), self.clear_history()), **btn_style)
        self.clear_history_btn.pack(side="left", padx=4, pady=6)
        self.change_role_btn = tk.Button(btn_group, text="Change Role", command=lambda: (self.play_sound('click.wav'), self.change_role()), **btn_style)
        self.change_role_btn.pack(side="left", padx=4, pady=6)

        # Card status
        tk.Label(self.sidebar, text="Card Status", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=(0, 2), fill="x")
        self.remaining_label = tk.Label(self.sidebar, text="", justify="left", font=("Arial", 11), bg="#f5f5f5")
        self.remaining_label.pack(pady=5, fill="x")

        # History section
        history_frame = tk.Frame(self.sidebar, bg="#fff", bd=2, relief="groove")
        history_frame.pack(pady=(10, 0), padx=4, fill="both", expand=True)
        tk.Label(history_frame, text="History", font=("Arial", 12, "bold"), bg="#fff").pack(pady=(4, 0))
        self.history_text = tk.Text(history_frame, width=35, height=13, state="disabled", font=("Courier", 10), bg="#f9f9f9", bd=0, highlightthickness=0)
        self.history_text.pack(padx=6, pady=6, fill="both", expand=True)
        self.update_sidebar()

    def reset_score(self):
        self.player_score = 0
        self.cpu_score = 0
        self.app.player_score = 0
        self.app.cpu_score = 0
        self.update_sidebar()

    def clear_history(self):
        self.history = []
        self.update_sidebar()

    def change_role(self):
        self.app.show_role_selection()

    def get_score_text(self):
        return f"Player: {self.player_score}   CPU: {self.cpu_score}"

    def update_sidebar(self):
        # Update scoreboard
        self.score_label.config(text=self.get_score_text())
        # Update remaining
        self.remaining_label.config(text=f"Player cards: {len(self.player_hand)}\nCPU cards: {len(self.cpu_hand)}")
        # Update history
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, "end")
        for i, (p, c) in enumerate(self.history, 1):
            self.history_text.insert("end", f"Round {i}: You → {p:<8} | CPU → {c:<8}\n")
        self.history_text.config(state="disabled")

    def play_sound(self, filename):
        try:
            winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

    def play_round(self, player_choice):
        if self.game_over:
            return
        if player_choice not in self.player_hand:
            messagebox.showinfo("Error", "Card already used!")
            return
        self.player_hand.remove(player_choice)
        self.chosen_player_card = player_choice
        self.chosen_cpu_card = random.choice(self.cpu_hand)
        self.cpu_hand.remove(self.chosen_cpu_card)
        self.player_card_slot.config(image=self.card_images["Back"])
        self.cpu_card_slot.config(image=self.card_images["Back"])
        self.result_label.config(text="Cards placed... flipping!")
        self.update_player_hand()  # Refresh hand after play
        self.play_sound('flip.wav')
        self.root.after(1000, self.reveal_cards)

    def flip_card_animation(self, slot_label, from_card, to_card, callback=None, steps=8, delay=30):
        # Animate a card flip from 'from_card' to 'to_card' on the given slot_label
        # Shrink, swap, expand
        pil_from = self.pil_images[from_card]
        pil_to = self.pil_images[to_card]
        w, h = pil_from.size
        images = []
        # Shrink phase
        for i in range(steps):
            scale = 1 - (i / steps)
            new_w = max(1, int(w * scale))
            img = pil_from.resize((new_w, h))
            images.append(ImageTk.PhotoImage(img))
        # Expand phase (after swap)
        for i in range(steps):
            scale = (i + 1) / steps
            new_w = max(1, int(w * scale))
            img = pil_to.resize((new_w, h))
            images.append(ImageTk.PhotoImage(img))
        def animate(idx=0):
            if idx < len(images):
                slot_label.config(image=images[idx])
                slot_label.image = images[idx]  # Prevent garbage collection
                self.root.after(delay, lambda: animate(idx + 1))
            else:
                slot_label.config(image=self.card_images[to_card])
                slot_label.image = self.card_images[to_card]
                self.play_sound('flip.wav')
                if callback:
                    callback()
        animate()

    def reveal_cards(self):
        # Animate both flips, then update result and sidebar
        def after_both():
            self.result_label.config(
                text=f"You played: {self.chosen_player_card} | CPU played: {self.chosen_cpu_card}"
            )
            self.history.append((self.chosen_player_card, self.chosen_cpu_card))
            self.update_sidebar()
            winner = self.determine_winner(self.chosen_player_card, self.chosen_cpu_card)
            self.root.after(1000, lambda: self.show_result(winner))
        # Animate player, then CPU, then call after_both
        def flip_cpu():
            self.flip_card_animation(
                self.cpu_card_slot, "Back", self.chosen_cpu_card, after_both
            )
        self.flip_card_animation(
            self.player_card_slot, "Back", self.chosen_player_card, flip_cpu
        )

    def show_result(self, winner):
        # Modern, minimal result banner instead of popup
        self.game_over = False
        if winner == "Player":
            self.player_score += 1
            self.app.player_score = self.player_score
            self.update_sidebar()
            self.show_result_banner("🎉 You win the game!", "#27ae60")
            self.play_sound('win.wav')
            self.show_new_game_button()
            self.game_over = True
        elif winner == "CPU":
            self.cpu_score += 1
            self.app.cpu_score = self.cpu_score
            self.update_sidebar()
            self.show_result_banner("💀 CPU wins the game!", "#c0392b")
            self.play_sound('lose.wav')
            self.show_new_game_button()
            self.game_over = True
        else:
            self.update_sidebar()
            self.show_result_banner("⚖️ Draw! Continue to next round...", "#FFD700")
            self.play_sound('draw.wav')
        if not self.player_hand or not self.cpu_hand:
            self.show_result_banner("🃏 All cards used. It's a draw.", "#888")
            self.play_sound('draw.wav')
            self.show_new_game_button()
            self.game_over = True

    def determine_winner(self, card1, card2):
        rules = {
            ("Emperor", "Citizen"): "Emperor",
            ("Citizen", "Slave"): "Citizen",
            ("Slave", "Emperor"): "Slave"
        }

        if card1 == card2:
            return "Draw"

        if (card1, card2) in rules:
            return "Player" if rules[(card1, card2)] == card1 else "CPU"
        elif (card2, card1) in rules:
            return "Player" if rules[(card2, card1)] == card1 else "CPU"
        else:
            return "Draw"

    def show_new_game_button(self):
        btn = tk.Button(self.main_frame, text="Play Again", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                        command=lambda: (self.play_sound('click.wav'), self.play_again()))
        btn.pack(pady=20)

    def play_again(self):
        # Start a new game with the same roles and keep the score by recreating the ECardGame instance
        self.game_over = False
        self.app.start_game(self.role, self.app.player_score, self.app.cpu_score)

    def show_result_banner(self, text, color):
        self.result_banner.config(text=text, fg=color, bg="#222")
        self.result_banner.after(2500, lambda: self.result_banner.config(text=""))


if __name__ == "__main__":
    root = tk.Tk()
    app = ECardApp(root)
    root.mainloop()
