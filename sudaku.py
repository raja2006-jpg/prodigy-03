import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

SAMPLE_PUZZLES = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],
    ]
]

class SudokuSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.pencil_marks = [[set() for _ in range(9)] for _ in range(9)]
        self.undo_stack = []
        self.redo_stack = []
        self.timer_running = False
        self.start_time = None
        self.timer_label = None
        self.theme = "light"
        self.selected_cell = (0, 0)
        # Create a master frame to hold everything
        self.master_frame = tk.Frame(self.root)
        self.master_frame.pack(fill="both", expand=True)
        # Board frame (labels + grid)
        self.create_grid_labels()
        self.create_grid()
        # Controls row
        self.create_controls_row()
        # Status bar
        self.create_status_bar()
    def create_grid_labels(self):
        # Create a parent frame for labels and grid inside master_frame
        self.board_frame = tk.Frame(self.master_frame)
        self.board_frame.pack(side="top", fill="x", pady=2)
        label_font = ("Consolas", 18, "bold")
        cell_width = 3
        cell_height = 1
        self.col_labels = []
        self.row_labels = []
        # Column labels (A-I)
        for j in range(9):
            lbl = tk.Label(self.board_frame, text=chr(65+j), font=label_font, bg="#ddd", width=cell_width, height=cell_height, anchor="center")
            lbl.grid(row=0, column=j+1, sticky="nsew", padx=0, pady=0)
            self.col_labels.append(lbl)
        # Row labels (1-9)
        for i in range(9):
            lbl = tk.Label(self.board_frame, text=str(i+1), font=label_font, bg="#ddd", width=cell_width, height=cell_height, anchor="center")
            lbl.grid(row=i+1, column=0, sticky="nsew", padx=0, pady=0)
            self.row_labels.append(lbl)
        # Make all cells expand equally
        for i in range(10):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)
        self.root.bind('<Key>', self.handle_arrow_keys)
        self.root.bind('<Control-z>', self.undo)
        self.root.bind('<Control-y>', self.redo)
        self.root.bind('<Button-1>', self.handle_mouse_click, add='+')

    def create_grid(self):
        # Place Sudoku cells in the same board_frame as labels
        self.grid_frame = tk.Frame(self.board_frame, bg="#888")
        self.grid_frame.grid(row=1, column=1, columnspan=9, rowspan=9, padx=0, pady=0, sticky="nsew")
        entry_font = ("Consolas", 18)
        self.cell_frames = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                # Subgrid coloring
                if (i//3 + j//3) % 2 == 0:
                    cell_bg = "#f8f8ff"
                else:
                    cell_bg = "#eaeaf6"
                cell_frame = tk.Frame(
                    self.grid_frame,
                    highlightbackground="#333",
                    highlightcolor="#333",
                    highlightthickness=2 if (i % 3 == 0 or j % 3 == 0) else 1,
                    bd=0,
                    bg=cell_bg
                )
                cell_frame.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
                entry = tk.Entry(cell_frame, width=3, font=entry_font, justify='center', validate='key', relief="flat")
                entry['validatecommand'] = (self.root.register(self.validate_entry), '%P', '%W')
                entry.pack(padx=0, pady=0, expand=True, fill='both')
                entry.bind('<FocusIn>', lambda e, x=i, y=j: self.on_cell_focus(x, y))
                entry.bind('<Key>', lambda e, x=i, y=j: self.handle_cell_key(e, x, y))
                entry.bind('<Enter>', lambda e, x=i, y=j: self.on_cell_hover(x, y))
                entry.bind('<Leave>', lambda e: self.on_cell_hover_leave())
                self.entries[i][j] = entry
                self.cell_frames[i][j] = cell_frame
        # Make grid responsive
        for i in range(9):
            self.grid_frame.grid_rowconfigure(i, weight=1)
            self.grid_frame.grid_columnconfigure(i, weight=1)

    def create_controls_row(self):
        # Controls row below the board_frame, inside master_frame
        controls = tk.Frame(self.master_frame)
        controls.pack(side="top", fill="x", pady=2)
        # Timer
        self.timer_label = tk.Label(controls, text="Time: 00:00")
        self.timer_label.pack(side="left", padx=4)
        self.start_timer()
        # Preset dropdown
        self.preset_var = tk.StringVar(value="Select Puzzle")
        preset_menu = ttk.Combobox(controls, textvariable=self.preset_var, values=[f"Sample {i+1}" for i in range(len(SAMPLE_PUZZLES))], state="readonly", width=12)
        preset_menu.pack(side="left", padx=4)
        preset_menu.bind("<<ComboboxSelected>>", lambda e: self.load_preset(self.preset_var.get()))
        # Theme toggle
        theme_btn = ttk.Button(controls, text="Toggle Theme", command=self.toggle_theme)
        theme_btn.pack(side="left", padx=4)
        # Button panel
        solve_btn = ttk.Button(controls, text="Solve", command=self.solve)
        solve_btn.pack(side="left", padx=4)
        clear_btn = ttk.Button(controls, text="Clear", command=self.clear_board)
        clear_btn.pack(side="left", padx=4)
        step_btn = ttk.Button(controls, text="Step", command=self.step_solve)
        step_btn.pack(side="left", padx=4)
        undo_btn = ttk.Button(controls, text="Undo", command=self.undo)
        undo_btn.pack(side="left", padx=4)
        redo_btn = ttk.Button(controls, text="Redo", command=self.redo)
        redo_btn.pack(side="left", padx=4)
    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.master_frame, textvariable=self.status_var, anchor='w', relief='sunken', bg='#eee')
        self.status_bar.pack(side="top", fill="x")
        self.set_status("Ready.")

    def set_status(self, msg):
        self.status_var.set(msg)
    def on_cell_hover(self, i, j):
        self.hovered_cell = (i, j)
        # Highlight row/col labels
        for idx, lbl in enumerate(self.col_labels):
            if idx == j:
                lbl.config(bg="#b3d1ff")
            else:
                lbl.config(bg="#ddd")
        for idx, lbl in enumerate(self.row_labels):
            if idx == i:
                lbl.config(bg="#b3d1ff")
            else:
                lbl.config(bg="#ddd")
        self.update_highlight()

    def on_cell_hover_leave(self):
        self.hovered_cell = None
        # Remove label highlight
        for lbl in self.col_labels:
            lbl.config(bg="#ddd")
        for lbl in self.row_labels:
            lbl.config(bg="#ddd")
        self.update_highlight()
    def create_theme_toggle(self):
        theme_btn = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        theme_btn.grid(row=2, column=5, columnspan=1, pady=2)

    def create_timer(self):
        self.timer_label = tk.Label(self.root, text="Time: 00:00")
        self.timer_label.grid(row=2, column=0, columnspan=2, pady=2)
        self.start_timer()

    def start_timer(self):
        import time
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        import time
        if self.timer_running:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")
            self.root.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False

    def create_preset_dropdown(self):
        self.preset_var = tk.StringVar(value="Select Puzzle")
        preset_menu = tk.OptionMenu(self.root, self.preset_var, *[f"Sample {i+1}" for i in range(len(SAMPLE_PUZZLES))], command=self.load_preset)
        preset_menu.grid(row=3, column=0, columnspan=2, pady=10)

    def load_preset(self, value):
        idx = int(value.split()[-1]) - 1
        self.set_board(SAMPLE_PUZZLES[idx])
        self.start_timer()

    def validate_entry(self, value, widget_name):
        # Only allow 1-9 or empty
        if value == "":
            self.set_entry_bg(widget_name, self.get_cell_bg(widget_name))
            return True
        if value.isdigit() and 1 <= int(value) <= 9:
            self.set_entry_bg(widget_name, self.get_cell_bg(widget_name))
            return True
        self.set_entry_bg(widget_name, "#ffcccc")
        self.root.after(100, lambda: self.clear_invalid(widget_name))
        return False
    def get_cell_bg(self, widget_name):
        # Highlight row/col/subgrid for selected or hovered cell, and highlight duplicates
        try:
            widget = self.root.nametowidget(widget_name)
            for i in range(9):
                for j in range(9):
                    if self.entries[i][j] == widget:
                        cell = (i, j)
                        # Highlight hovered cell if present
                        ref = self.hovered_cell if hasattr(self, 'hovered_cell') and self.hovered_cell else self.selected_cell
                        if cell == ref:
                            return "#e0e0ff" if self.theme == "light" else "#333366"
                        elif i == ref[0] or j == ref[1] or (i//3, j//3) == (ref[0]//3, ref[1]//3):
                            return "#f0f0ff" if self.theme == "light" else "#222244"
                        # Highlight duplicates
                        val = self.entries[i][j].get()
                        if val and self.is_duplicate(i, j, val):
                            return "#ffdddd"
            return "white" if self.theme == "light" else "#222"
        except Exception:
            return "white"

    def is_duplicate(self, row, col, val):
        # Check for duplicate in row, col, or subgrid
        for j in range(9):
            if j != col and self.entries[row][j].get() == val:
                return True
        for i in range(9):
            if i != row and self.entries[i][col].get() == val:
                return True
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row+3):
            for j in range(start_col, start_col+3):
                if (i, j) != (row, col) and self.entries[i][j].get() == val:
                    return True
        return False
    def on_cell_focus(self, i, j):
        self.selected_cell = (i, j)
        self.set_status(f"Cell {chr(65+j)}{i+1} selected.")
        self.update_highlight()

    def update_highlight(self):
        for x in range(9):
            for y in range(9):
                widget = self.entries[x][y]
                # Highlight selected cell with thicker border
                if (x, y) == self.selected_cell:
                    self.cell_frames[x][y].config(highlightbackground="#0077ff", highlightcolor="#0077ff", highlightthickness=4)
                else:
                    self.cell_frames[x][y].config(highlightbackground="#333", highlightcolor="#333", highlightthickness=2 if (x % 3 == 0 or y % 3 == 0) else 1)
                widget.config(bg=self.get_cell_bg(str(widget)))
                # Show pencil marks if present
                if not widget.get() and self.pencil_marks[x][y]:
                    widget.config(fg="#888")
                    widget.delete(0, tk.END)
                    widget.insert(0, ''.join(sorted(str(n) for n in self.pencil_marks[x][y])))
                else:
                    widget.config(fg="black" if self.theme == "light" else "white")
                # Tooltip for cell
                widget.tooltip = f"Cell {chr(65+y)}{x+1}"
    def handle_mouse_click(self, event):
        widget = event.widget
        for i in range(9):
            for j in range(9):
                if self.entries[i][j] == widget:
                    self.selected_cell = (i, j)
                    self.update_highlight()
                    return
    def handle_cell_key(self, event, i, j):
        # Pencil mark mode: Shift+number
        if event.state & 0x0001 and event.char in '123456789':
            n = int(event.char)
            if n in self.pencil_marks[i][j]:
                self.pencil_marks[i][j].remove(n)
            else:
                self.pencil_marks[i][j].add(n)
            self.entries[i][j].delete(0, tk.END)
            self.entries[i][j].insert(0, ''.join(sorted(str(x) for x in self.pencil_marks[i][j])))
            self.entries[i][j].config(fg="#888")
            return "break"
        # Normal entry: record undo
        if event.char in '123456789' or event.keysym == 'BackSpace':
            self.push_undo()
            self.pencil_marks[i][j].clear()
    def push_undo(self):
        # Save current board and pencil marks
        import copy
        board = [[self.entries[i][j].get() for j in range(9)] for i in range(9)]
        pencils = copy.deepcopy(self.pencil_marks)
        self.undo_stack.append((board, pencils))
        if len(self.undo_stack) > 100:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def pop_undo(self):
        if self.undo_stack:
            return self.undo_stack.pop()
        return None

    def undo(self, event=None):
        if not self.undo_stack:
            return
        import copy
        board, pencils = self.undo_stack.pop()
        redo_board = [[self.entries[i][j].get() for j in range(9)] for i in range(9)]
        redo_pencils = copy.deepcopy(self.pencil_marks)
        self.redo_stack.append((redo_board, redo_pencils))
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, board[i][j])
        self.pencil_marks = copy.deepcopy(pencils)
        self.update_highlight()

    def redo(self, event=None):
        if not self.redo_stack:
            return
        import copy
        board, pencils = self.redo_stack.pop()
        self.push_undo()
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].insert(0, board[i][j])
        self.pencil_marks = copy.deepcopy(pencils)
        self.update_highlight()

    def set_entry_bg(self, widget_name, color):
        widget = self.root.nametowidget(widget_name)
        widget.config(bg=color)

    def clear_invalid(self, widget_name):
        widget = self.root.nametowidget(widget_name)
        widget.delete(0, tk.END)
        widget.config(bg="white")

    def handle_arrow_keys(self, event):
        widget = self.root.focus_get()
        for i in range(9):
            for j in range(9):
                if self.entries[i][j] == widget:
                    if event.keysym == 'Up' and i > 0:
                        self.entries[i-1][j].focus_set()
                    elif event.keysym == 'Down' and i < 8:
                        self.entries[i+1][j].focus_set()
                    elif event.keysym == 'Left' and j > 0:
                        self.entries[i][j-1].focus_set()
                    elif event.keysym == 'Right' and j < 8:
                        self.entries[i][j+1].focus_set()
                    return

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(bg=self.get_cell_bg(str(self.entries[i][j])))
                self.pencil_marks[i][j].clear()
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.start_timer()

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == '' or not val.isdigit():
                    row.append(0)
                else:
                    try:
                        v = int(val)
                        if not (1 <= v <= 9):
                            raise ValueError
                        row.append(v)
                    except ValueError:
                        self.entries[i][j].config(bg="#ffcccc")
                        messagebox.showerror("Invalid input", f"Cell ({i+1},{j+1}) must be a number between 1-9.")
                        return None
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))
                self.entries[i][j].config(bg=self.get_cell_bg(str(self.entries[i][j])))
                self.pencil_marks[i][j].clear()
        self.update_highlight()

    def solve(self):
        board = self.get_board()
        if board and self.solve_sudoku(board):
            self.set_board(board)
            messagebox.showinfo("Success", "Sudoku Solved!")
            self.stop_timer()
        else:
            messagebox.showerror("Error", "No solution exists or invalid puzzle.")
    def step_solve(self):
        # Step-by-step solver using generator
        board = self.get_board()
        if not board:
            return
        self.step_solver = self.solve_sudoku_steps(board)
        self.do_step()

    def do_step(self):
        try:
            next(self.step_solver)
            self.set_board(self.get_board())
            self.root.after(200, self.do_step)
        except StopIteration:
            self.set_board(self.get_board())
            messagebox.showinfo("Step Solver", "Step-by-step solve complete!")

    def solve_sudoku_steps(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            self.set_board(board)
                            yield
                            if any(0 in r for r in board):
                                yield from self.solve_sudoku_steps(board)
                            if all(all(cell != 0 for cell in r) for r in board):
                                return
                            board[row][col] = 0
                    return
    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        for i in range(9):
            for j in range(9):
                entry = self.entries[i][j]
                entry.config(bg=self.get_cell_bg(str(entry)), fg="white" if self.theme == "dark" else "black")
        self.root.config(bg="#222" if self.theme == "dark" else "white")
        self.timer_label.config(bg="#222" if self.theme == "dark" else "white", fg="white" if self.theme == "dark" else "black")
        self.update_highlight()

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True

# Run the GUI
root = tk.Tk()
app = SudokuSolverGUI(root)
root.mainloop()
# prodigy-03
