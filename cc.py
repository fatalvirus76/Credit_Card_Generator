import random
from luhn import verify, generate, append
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu, Text, Scrollbar, END, VERTICAL, RIGHT, Y

# Generate credit card numbers based on the selected type and count
def generate_cards():
    custom_prefix = custom_prefix_entry.get().strip()
    card_type = card_type_var.get()
    try:
        count = int(count_entry.get())
        if count <= 0:
            result_text.insert(END, "Count must be a positive integer.\n")
            return
    except ValueError:
        result_text.insert(END, "Invalid count. Please enter a positive integer.\n")
        return

    prefixes = {
        "Visa": ["4"],
        "MasterCard": ["51", "52", "53", "54", "55"],
        "American Express": ["34", "37"],
        "Discover": ["6011", "622126", "622127", "622128", "622129", "62213", "62214", "62215", "62216", "62217", "62218", "62219", "6222", "6223", "6224", "6225", "6226", "6227", "6228", "62290", "62291", "622920", "622921", "622922", "622923", "622924", "622925"],
    }
    lengths = {
        "Visa": 16,
        "MasterCard": 16,
        "American Express": 15,
        "Discover": 16,
    }

    if custom_prefix:
        if not custom_prefix.isdigit() or len(custom_prefix) < 6 or len(custom_prefix) >= lengths.get(card_type, 16):
            result_text.insert(END, "Invalid custom prefix. It must be numeric and 6 digits long or shorter.\n")
            return
        prefix_choices = [custom_prefix]
        length = lengths.get(card_type, 16)
    else:
        if card_type not in prefixes:
            result_text.insert(END, "Invalid card type selected.\n")
            return
        prefix_choices = prefixes[card_type]
        length = lengths[card_type]

    result_text.delete(1.0, END)
    for _ in range(count):
        prefix = random.choice(prefix_choices)
        remaining_length = length - len(prefix) - 1
        partial_number = prefix + ''.join(random.choice('0123456789') for _ in range(remaining_length))
        card_number = append(partial_number)
        if verify(card_number):
            result_text.insert(END, f"{card_number}\n")
        else:
            result_text.insert(END, "Failed to generate a valid card number.\n")

# GUI Setup
root = Tk()
root.title("Credit Card Generator")

# Card type selection
Label(root, text="Card Type:").grid(row=0, column=0, padx=10, pady=5)
card_type_var = StringVar(value="Visa")
card_type_menu = OptionMenu(root, card_type_var, "Visa", "MasterCard", "American Express", "Discover")
card_type_menu.grid(row=0, column=1, padx=10, pady=5)

# Custom prefix entry
Label(root, text="Custom Prefix (optional):").grid(row=1, column=0, padx=10, pady=5)
custom_prefix_entry = Entry(root)
custom_prefix_entry.grid(row=1, column=1, padx=10, pady=5)

# Number of cards to generate
Label(root, text="Count:").grid(row=2, column=0, padx=10, pady=5)
count_entry = Entry(root)
count_entry.grid(row=2, column=1, padx=10, pady=5)

# Generate button
generate_button = Button(root, text="Generate", command=generate_cards)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Result display
Label(root, text="Generated Cards:").grid(row=4, column=0, columnspan=2)
result_text = Text(root, height=10, width=40)
result_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
scrollbar = Scrollbar(root, orient=VERTICAL, command=result_text.yview)
scrollbar.grid(row=5, column=2, sticky='ns')
result_text.config(yscrollcommand=scrollbar.set)

# Start GUI loop
root.mainloop()

