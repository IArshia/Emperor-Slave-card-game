import tkinter as tk
from PIL import Image, ImageTk

# Path to your saved image (use the actual file path if different)
IMAGE_PATH = "D:\projects\Emperor-Slave-card-game\citizen.jpg"

def on_card_click(card_name):
    result_label.config(text=f"You selected: {card_name}")

root = tk.Tk()
root.title("E-Card Game")

# Load and display the image
image = Image.open(IMAGE_PATH)
photo = ImageTk.PhotoImage(image)

canvas = tk.Canvas(root, width=image.width, height=image.height)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=photo)

# Buttons below the image to simulatEmperor-Slave-card-game clicks
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

for card in ["Emperor", "Citizen", "Slave"]:
    btn = tk.Button(button_frame, text=card, command=lambda c=card: on_card_click(c))
    btn.pack(side="left", padx=10)

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()

card_paths = {
    "Emperor": "D:\projects\Emperor-Slave-card-game\emperor.jpg",
    "Citizen": "D:\projects\Emperor-Slave-card-game\citizen.jpg",
    "Slave": "D:\projects\Emperor-Slave-card-game\slave.jpg",
    "Back": r'D:\projects\Emperor-Slave-card-game\back.jpg'  
}