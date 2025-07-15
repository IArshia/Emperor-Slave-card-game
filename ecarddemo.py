import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

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
        self.show_role_selection()

    def show_role_selection(self):
        self.clear_screen()

        title = tk.Label(self.root, text="Choose Your Role", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        tk.Button(button_frame, text="Play as Emperor", font=("Arial", 14),
                  command=lambda: self.start_game("Emperor"), width=20).pack(padx=20, pady=10)

        tk.Button(button_frame, text="Play as Slave", font=("Arial", 14),
                  command=lambda: self.start_game("Slave"), width=20).pack(padx=20, pady=10)

    def start_game(self, role):
        self.clear_screen()
        self.game = ECardGame(self.root, self, role, self.card_images)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class ECardGame:
    def __init__(self, root, app, role, card_images):
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

        # Main layout frames
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side="left", padx=10)

        self.sidebar = tk.Frame(root)
        self.sidebar.pack(side="right", padx=10, fill="y")

        self.label = tk.Label(self.main_frame, text=f"You are playing as: {self.role}", font=("Arial", 14))
        self.label.pack(pady=10)

        # Table layout
        self.table_frame = tk.Frame(self.main_frame)
        self.table_frame.pack(pady=10)

        self.cpu_card_slot = tk.Label(self.table_frame, image=self.card_images["Back"])
        self.cpu_card_slot.grid(row=0, column=1, padx=10)

        self.vs_label = tk.Label(self.table_frame, text="VS", font=("Arial", 16, "bold"))
        self.vs_label.grid(row=1, column=1)

        self.player_card_slot = tk.Label(self.table_frame, image=self.card_images["Back"])
        self.player_card_slot.grid(row=2, column=1, padx=10)

        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.result_label = tk.Label(self.main_frame, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.create_card_buttons()
        self.create_sidebar()

    def init_hand(self, role):
        if role == "Emperor":
            return ["Emperor"] + ["Citizen"] * 4
        else:
            return ["Slave"] + ["Citizen"] * 4

    def create_card_buttons(self):
        for card_name in set(self.player_hand):
            btn = tk.Button(
                self.button_frame,
                image=self.card_images[card_name],
                command=lambda c=card_name: self.play_round(c)
            )
            btn.pack(side="left", padx=10)

    def create_sidebar(self):
        tk.Label(self.sidebar, text="Card Status", font=("Arial", 14, "bold")).pack()

        self.remaining_label = tk.Label(self.sidebar, text="", justify="left", font=("Arial", 11))
        self.remaining_label.pack(pady=5)

        tk.Label(self.sidebar, text="History", font=("Arial", 12, "bold")).pack(pady=5)
        self.history_text = tk.Text(self.sidebar, width=35, height=15, state="disabled", font=("Courier", 10))
        self.history_text.pack()

        self.update_sidebar()

    def update_sidebar(self):
        # Update remaining
        remaining_text = f"Player cards: {len(self.player_hand)}\nCPU cards: {len(self.cpu_hand)}"
        self.remaining_label.config(text=remaining_text)

        # Update history
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, "end")
        for i, (p, c) in enumerate(self.history, 1):
            self.history_text.insert("end", f"Round {i}: You → {p:<8} | CPU → {c:<8}\n")
        self.history_text.config(state="disabled")

    def play_round(self, player_choice):
        if player_choice not in self.player_hand:
            messagebox.showinfo("Error", "Card already used!")
            return

        # Remove card
        self.player_hand.remove(player_choice)
        self.chosen_player_card = player_choice

        self.chosen_cpu_card = random.choice(self.cpu_hand)
        self.cpu_hand.remove(self.chosen_cpu_card)

        # Show back first
        self.player_card_slot.config(image=self.card_images["Back"])
        self.cpu_card_slot.config(image=self.card_images["Back"])
        self.result_label.config(text="Cards placed... flipping!")

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
        if winner == "Player":
            messagebox.showinfo("Result", "🎉 You win the game!")
            self.show_new_game_button()
        elif winner == "CPU":
            messagebox.showinfo("Result", "💀 CPU wins the game!")
            self.show_new_game_button()
        else:
            messagebox.showinfo("Result", "⚖️ Draw! Continue to next round...")

        if not self.player_hand or not self.cpu_hand:
            messagebox.showinfo("Result", "🃏 All cards used. It's a draw.")
            self.show_new_game_button()

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
                        command=self.app.show_role_selection)
        btn.pack(pady=20)  
    


if __name__ == "__main__":
    root = tk.Tk()
    app = ECardApp(root)
    root.mainloop()
