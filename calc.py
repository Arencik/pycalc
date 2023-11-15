import tkinter as tk

LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
SMALL_FONT_STYLE = ("Arial", 16)
LARGE_FONT_STYLE = ("Arial", 40, "bold")
WHITE = "#FFFFFF"
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)
OFF_WHITE = "#F8FAFF"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("275x667")
        self.window.resizable(0,0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.total_label, self.label = self.create_display_labels()
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_clear_button()
        self.create_equals_button()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self) -> None:
        """Binds events to relevant keys"""
        self.window.bind("<Return>", lambda event: self.evaluate())

        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self) -> None:
        """Creates clear, equals, sqrt and square buttons"""
        self.create_clear_button()
        self.create_equals_button()
        self.create_sqrt_button()
        self.create_square_button()

    def create_display_labels(self) -> tuple[tk.Label, tk.Label]:
        """Creates display labels"""
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")
        return total_label, label

    def create_display_frame(self) -> tk.Frame:
        """Creates frame for display"""
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame
    
    def add_to_expression(self, value: float) -> None:
        """Adds given value to created expression"""
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self) -> None:
        """Creates grid buttons for each digit"""
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit),
                               bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator: str) -> None:
        """Appends operator to the created expression"""
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self) -> None:
        """Creates buttons for the operators"""
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol,
                               bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command= lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self) -> None:
        """Cleares the display label"""
        self.current_expression=""
        self.total_expression=""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self) -> None:
        """Creates and adds clear button to the button frame"""
        button = tk.Button(self.buttons_frame, text='C', bg=OFF_WHITE,
                           fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, columnspan=3,  sticky=tk.NSEW)

    def square(self) -> None:
        """Squares the current expression"""
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self) -> None:
        """Creates the square button"""
        button = tk.Button(self.buttons_frame, text='x\u00b2', bg=OFF_WHITE,
                           fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self) -> None:
        """Operation for square root of the current expression"""
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self) -> None:
        """Creates the square root button"""
        button = tk.Button(self.buttons_frame, text='\u221ax', bg=OFF_WHITE,
                           fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self) -> None:
        """Evaluates the correctness of the given expression
            If the expression is invalid, Updates the label as "Error"
        """
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self) -> None:
        """Creates equeals button"""
        button = tk.Button(self.buttons_frame, text='=', bg=OFF_WHITE,
                           fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2,  sticky=tk.NSEW)

    def create_buttons_frame(self) -> tk.Frame:
        """Creates frame for buttons"""
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self) -> None:
        """Updates the total display"""
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self) -> None:
        """Updates the basic label for adding expressions"""
        self.label.config(text=self.current_expression[:11])

    def run(self) -> None:
        """Runs the calc"""
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
