import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import random

# Function to fetch Mega Millions numbers from a website
def get_mega_millions_numbers():
    url = "https://www.lottostrategies.com/cgi-bin/winning_of_past_month/100/101/WV/West-Virginia-WV-Mega-Millions-lottery-results.html"
    
    try:
        # Send a GET request to the website with retries
        for _ in range(3):
            response = requests.get(url)
            if response.status_code == 200:
                break
        else:
            raise Exception("Failed to retrieve data after multiple attempts.")

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the Mega Millions numbers on the page (adjust this based on the actual structure of the website)
        mega_millions_numbers = soup.find('div', {'id': 'winning_numbers'}).text.strip().split()

        return mega_millions_numbers
    except Exception as e:
        return None

# Function to generate random Mega Millions numbers
def generate_mega_millions_numbers(num_sets=1, main_set_range=(1, 70), mega_ball_range=(1, 25)):
    generated_sets = []

    for _ in range(num_sets):
        # Generate five random numbers for the main set
        main_numbers = random.sample(range(main_set_range[0], main_set_range[1] + 1), 5)

        # Generate a random number for the Mega Ball set
        mega_ball_number = random.randint(mega_ball_range[0], mega_ball_range[1])

        generated_sets.append((main_numbers, mega_ball_number))

    return generated_sets

# Function to save Mega Millions results to a file
def save_mega_millions_to_file(mega_millions_sets, filename='mega_millions_results.txt'):
    with open(filename, 'a') as file:
        for main_numbers, mega_ball_number in mega_millions_sets:
            file.write(f"Main Numbers: {main_numbers}, Mega Ball: {mega_ball_number}\n")

# Event handler for the "Generate Mega Millions Numbers" button
def on_generate_mega_millions_button():
    try:
        num_sets = int(num_sets_entry.get())
        mega_millions_results = generate_mega_millions_numbers(num_sets=num_sets)

        if mega_millions_results:
            # Enable the result_text widget for editing
            result_text.config(state=tk.NORMAL)
            # Clear existing content
            result_text.delete("1.0", tk.END)
            # Display generated Mega Millions numbers
            result_text.insert(tk.END, f"Mega Millions Numbers:\n")
            for i, (main_numbers, mega_ball_number) in enumerate(mega_millions_results, 1):
                result_text.insert(tk.END, f"Set {i}: Main Numbers: {main_numbers}, Mega Ball: {mega_ball_number}\n")

            # Save results to a file
            save_mega_millions_to_file(mega_millions_results, 'mega_millions_results.txt')

            # Display a message indicating that results are saved
            result_text.insert(tk.END, "\nResults saved to mega_millions_results.txt")
            # Disable the result_text widget for further editing
            result_text.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for 'Number of Sets'.")

# Event handler for the "Clear Mega Millions Results" button
def on_clear_mega_millions_button():
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.config(state=tk.DISABLED)

# Create the main window
window = tk.Tk()
window.title("Mega Millions Number Generator")

# Set window dimensions
window.geometry("400x400")

# Set window background color
window.configure(bg="#F5F5F5")

# Add a logo (replace 'images/mega_millions.png' with the actual path to the Mega Millions logo)
logo_image = tk.PhotoImage(file="images/megamillions.png")
logo_label = tk.Label(window, image=logo_image, bg="#F5F5F5")
logo_label.pack(anchor="center", padx=10, pady=10)

# Create and pack widgets with improved styling
tk.Label(window, text="Number of Sets:", font=("Helvetica", 12), bg="#F5F5F5").pack(pady=10)
num_sets_entry = tk.Entry(window, font=("Helvetica", 12), width=5)
num_sets_entry.pack(pady=10)

generate_mega_millions_button = tk.Button(window, text="Generate Numbers", command=on_generate_mega_millions_button, font=("Helvetica", 12), bg="blue", fg="white")
generate_mega_millions_button.pack(pady=15)

clear_mega_millions_button = tk.Button(window, text="Clear Results", command=on_clear_mega_millions_button, font=("Helvetica", 12), bg="white", fg="black")
clear_mega_millions_button.pack(pady=15)

result_text = tk.Text(window, height=10, width=40, font=("Helvetica", 10), state=tk.DISABLED, bg="#F5F5F5")
result_text.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
