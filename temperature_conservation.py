import tkinter as tk
from tkinter import ttk, messagebox

def convert_temperature():
    try:
        temp = float(entry_temp.get())
        unit = combo_unit.get()

        if unit == "Celsius (°C)":
            fahrenheit = (temp * 9/5) + 32
            kelvin = temp + 273.15
            result_text = f"🌡️ {temp:.2f} °C = {fahrenheit:.2f} °F\n🌡️ {temp:.2f} °C = {kelvin:.2f} K"
        elif unit == "Fahrenheit (°F)":
            celsius = (temp - 32) * 5/9
            kelvin = celsius + 273.15
            result_text = f"🌡️ {temp:.2f} °F = {celsius:.2f} °C\n🌡️ {temp:.2f} °F = {kelvin:.2f} K"
        elif unit == "Kelvin (K)":
            celsius = temp - 273.15
            fahrenheit = (celsius * 9/5) + 32
            result_text = f"🌡️ {temp:.2f} K = {celsius:.2f} °C\n🌡️ {temp:.2f} K = {fahrenheit:.2f} °F"
        else:
            result.set("❌ Please select a valid unit.")
            return

        result.set(result_text)

    except ValueError:
        messagebox.showerror("Invalid Input", "⚠️ Please enter a valid numeric temperature.")

# GUI Setup
root = tk.Tk()
root.title("🌡️ Temperature Converter")
root.geometry("400x350")
root.configure(bg="#2C3E50")
root.resizable(False, False)

# Center the window on screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width/2) - (400/2))
y = int((screen_height/2) - (350/2))
root.geometry(f"+{x}+{y}")

# Header
tk.Label(root, text="Temperature Converter", font=("Helvetica", 18, "bold"),
         fg="#ECF0F1", bg="#2C3E50").pack(pady=20)

# Temperature Input
frame_input = tk.Frame(root, bg="#2C3E50")
frame_input.pack(pady=10)

tk.Label(frame_input, text="Enter Temperature:", font=("Arial", 12),
         fg="white", bg="#2C3E50").grid(row=0, column=0, padx=10)
entry_temp = tk.Entry(frame_input, font=("Arial", 12), width=15)
entry_temp.grid(row=0, column=1)

# Unit Selection
tk.Label(root, text="Select Original Unit:", font=("Arial", 12),
         fg="white", bg="#2C3E50").pack(pady=5)

combo_unit = ttk.Combobox(root, font=("Arial", 12), state="readonly",
                          values=["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"], width=20)
combo_unit.pack()

# Convert Button
tk.Button(root, text="Convert", font=("Arial", 12, "bold"),
          bg="#27AE60", fg="white", width=15, command=convert_temperature).pack(pady=15)

# Result Display
result = tk.StringVar()
label_result = tk.Label(root, textvariable=result, font=("Arial", 12, "bold"),
                        fg="#F1C40F", bg="#2C3E50", justify="center")
label_result.pack(pady=10)

# Footer
tk.Label(root, text="© Prodigy Infotech | GUI Task-01", font=("Arial", 8),
         fg="#BDC3C7", bg="#2C3E50").pack(side="bottom", pady=5)

root.mainloop()
