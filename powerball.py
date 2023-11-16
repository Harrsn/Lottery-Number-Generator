import tkinter as tk
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import random

# Function to fetch Powerball numbers from a website
def get_powerball_numbers():
    url = "https://www.lottostrategies.com/cgi-bin/winning_of_past_month/100/101/WV/West-Virginia-WV-Powerball-lottery-results.html"
    
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

        # Find the Powerball numbers on the page (adjust this based on the actual structure of the website)
        powerball_numbers = soup.find('div', {'id': 'winning_numbers'}).text.strip().split()

        return powerball_numbers
    except Exception as e:
        return None

# Function to generate random Powerball numbers
def generate_powerball_numbers(num_sets=1, main_set_range=(1, 69), powerball_range=(1, 26)):
    generated_sets = []

    for _ in range(num_sets):
        # Generate five random numbers for the main set
        main_numbers = random.sample(range(main_set_range[0], main_set_range[1] + 1), 5)

        # Generate a random number for the Powerball set
        powerball_number = random.randint(powerball_range[0], powerball_range[1])

        generated_sets.append((main_numbers, powerball_number))

    return generated_sets

# Function to save Powerball results to a file
def save_to_file(powerball_sets, filename='powerball_results.txt'):
    with open(filename, 'a') as file:
        for main_numbers, powerball_number in powerball_sets:
            file.write(f"Main Numbers: {main_numbers}, Powerball: {powerball_number}\n")

# Event handler for the "Generate Numbers" button
def on_generate_button():
    try:
        num_sets = int(num_sets_entry.get())
        powerball_results = generate_powerball_numbers(num_sets=num_sets)

        if powerball_results:
            # Enable the result_text widget for editing
            result_text.config(state=tk.NORMAL)
            # Clear existing content
            result_text.delete("1.0", tk.END)
            # Display generated Powerball numbers
            result_text.insert(tk.END, "Powerball Numbers:\n")
            for i, (main_numbers, powerball_number) in enumerate(powerball_results, 1):
                result_text.insert(tk.END, f"Set {i}: Main Numbers: {main_numbers}, Powerball: {powerball_number}\n")

            # Save results to a file
            save_to_file(powerball_results, 'powerball_results.txt')

            # Display a message indicating that results are saved
            result_text.insert(tk.END, "\nResults saved to powerball_results.txt")
            # Disable the result_text widget for further editing
            result_text.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for 'Number of Sets'.")

# Create the main window
window = tk.Tk()
window.title("Powerball Number Generator")

# Set window dimensions
window.geometry("400x400")

# Set window background color
window.configure(bg="#F5F5F5")

# Add a logo
logo_image = tk.PhotoImage(file="C:/Users/harrsn/Desktop/Lottery Python/powerball.png")
logo_label = tk.Label(window, image=logo_image, bg="#F5F5F5")
logo_label.pack(anchor="center", padx=10, pady=10)

# Create and pack widgets with improved styling
tk.Label(window, text="Number of Sets:", font=("Helvetica", 12), bg="#F5F5F5").pack(pady=10)
num_sets_entry = tk.Entry(window, font=("Helvetica", 12), width=5)
num_sets_entry.pack(pady=10)

generate_button = tk.Button(window, text="Generate Numbers", command=on_generate_button, font=("Helvetica", 12), bg="red", fg="white")
generate_button.pack(pady=15)

result_text = tk.Text(window, height=10, width=40, font=("Helvetica", 10), state=tk.DISABLED, bg="#F5F5F5")
result_text.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
