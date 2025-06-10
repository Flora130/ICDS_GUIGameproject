import tkinter as tk
import random
import time

class ClickTheColorGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Click The Color but Not the Word")
        self.colors = ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
        self.score = 0
        self.round_count = 0
        self.start_time = None
        self.end_time = None
        
        self.create_widgets()
        self.next_round()

    def create_widgets(self):
        self.color_label = tk.Label(self.master, text="", font=("Helvetica", 30))
        self.color_label.pack(pady=20)
        self.message_label = tk.Label(self.master, text="", font=("Helvetica", 16), fg="red")
        self.message_label.pack(pady=10)

        self.btn_frame = tk.Frame(self.master)
        self.btn_frame.pack(pady=10)

        self.buttons = []
        for color in self.colors:
            btn = tk.Button(self.btn_frame, text=color, bg=color, fg="black", font=("Helvetica", 14),
                            command=lambda c=color: self.check_answer(c))
            btn.pack(side=tk.LEFT, padx=10)
            self.buttons.append(btn)

        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Helvetica", 16))
        self.score_label.pack(pady=10)

        self.time_label = tk.Label(self.master, text="", font=("Helvetica", 16))
        self.time_label.pack(pady=10)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_game)
        self.quit_button.pack_forget()  # Hide quit button initially

    def next_round(self):
        self.round_count += 1
        if self.round_count > 10:
            self.end_time = time.time()
            self.end_game()
            return
        
        if self.start_time is None:
            self.start_time = time.time()

        self.color_label.config(text=random.choice(self.colors), fg=random.choice(self.colors))
        
    def check_answer(self, selected_color):
        actual_color = self.color_label.cget('fg')
        if selected_color == actual_color:
            self.message_label.config(text=" ")
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.next_round()
        else:
            self.message_label.config(text="Choose the color but not the name! Try again")
            self.score -= 1
            self.score_label.config(text=f"Score: {self.score}")

    # isa added is_game_over() and get_score()
    def is_game_over(self):
        return self.round_count >= 10

    def get_score(self):
        return self.score

    def end_game(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)  # Disable color buttons
        self.quit_button.pack(pady=10)  # Show quit button
        if self.start_time is not None and self.end_time is not None:
            time_taken = self.end_time - self.start_time
            self.time_label.config(text=f"Time taken: {time_taken:.2f} seconds")

    def quit_game(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    game = ClickTheColorGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
