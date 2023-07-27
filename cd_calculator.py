from typing import Optional, Union, Callable
import tkinter as tk

# CONSTANTS ------------------------------------------------------------------------------------------------------------
DAYS_PER_YEAR = 365.
MONTHS_PER_YEAR = 12
TERM_DEFAULT = '[Select a Term]'
TKINTER_WINDOW = Union[tk.Tk, tk.Toplevel]
EMPTY_DISPLAY = '$        '


# DEFINE FUNCTIONS -----------------------------------------------------------------------------------------------------
def unpack_images(image_strs: list[str], image_zoom: int = 1, image_shrink: int = 1):
    images = []
    for image_str in image_strs:
        image = tk.PhotoImage(file=image_str).zoom(image_zoom).subsample(image_shrink)
        images.append(image)
    return images


def generate_swapper(open_window: TKINTER_WINDOW, closed_window: TKINTER_WINDOW):
    def swap_windows():
        open_window.withdraw()
        closed_window.deiconify()
    return swap_windows


def validate_term(selection) -> bool:
    return selection.get() != TERM_DEFAULT


def generate_validated_swapper(open_window: TKINTER_WINDOW, closed_window: TKINTER_WINDOW,
                          validation_fun: Callable, validation_var: tk.Variable):
    swap_windows = generate_swapper(open_window, closed_window)

    def swap_after_validation():
        if validation_fun(validation_var):
            swap_windows()
    return swap_after_validation


def generate_exit_program(root):
    def exit_program():
        root.destroy()
    return exit_program


def calculate_cd(principal: float, rate: float, term: float) -> (float, float):
    """
    This function returns average monthly dividend and total amount at end of term.

    :param principal: float, the starting capital, dollars
    :param rate: float, the annual interest rate, fraction
    :param term: float, the term, months
    :return: (float, float), a Tuple of the mean monthly return and total at end of term
    """

    total = principal * (1 + rate / DAYS_PER_YEAR) ** (term * DAYS_PER_YEAR / MONTHS_PER_YEAR)
    mean_return = (total - principal) / term

    return mean_return, total


def generate_entry_calculator(cd_options, cd_selection, principal_entry, dividends_display, total_display):
    def calculate_cd_from_entry():
        selection = cd_selection.get()

        try:
            principal = float(principal_entry.get())
            rate, term = cd_options[selection]
            mean_return, total = calculate_cd(principal, rate, term)

            dividends_display['text'] = f'${mean_return:.2f}'
            total_display['text'] = f'${total:.2f}'
        except RuntimeError:
            dividends_display['text'] = EMPTY_DISPLAY
            total_display['text'] = EMPTY_DISPLAY

    return calculate_cd_from_entry


# DEFINE WINDOW CLASSES ------------------------------------------------------------------------------------------------
class RootWindow(tk.Tk):
    def __init__(
            self, title: Optional[str] = None, images: Optional[list[str]] = None,
            image_zoom: int = 1, image_shrink: int = 1
    ):
        super().__init__()

        # Assign title string
        if title is not None:
            self.title(title)

        # Add reference to images to ensure they do not fall out of scope
        if images is not None:
            self.images = unpack_images(images, image_zoom=image_zoom, image_shrink=image_shrink)


class Window(tk.Toplevel):
    def __init__(
            self, root, title: Optional[str] = None, images: Optional[list[str]] = None,
            image_zoom: int = 1, image_shrink: int = 1
    ):
        super().__init__(root)

        # Assign title string
        if title is not None:
            self.title(title)

        # Add reference to images to ensure they do not fall out of scope
        if images is not None:
            self.images = unpack_images(images, image_zoom=image_zoom, image_shrink=image_shrink)


# DATA -----------------------------------------------------------------------------------------------------------------
cd_options = {
    '8-Month': (0.0512, 8),
    '15-Month': (0.0512, 15),
    '29-Month': (0.0405, 29)
}

# INSTANTIATE WINDOWS --------------------------------------------------------------------------------------------------
window_selection = RootWindow(
    title="Certificate of Deposit Calculator", images=['bank_image.png'], image_shrink=4
)

window_calculation = Window(window_selection, title='Calculate CD Gains', images=['cd_image.png'], image_shrink=2)
# window_calculation.withdraw()  # Not open by default

# BUILD FIRST WINDOW (TERM SELECTION) ----------------------------------------------------------------------------------

# Create Frame for 1st Window
label_term = tk.Label(master=window_selection, text="Select a term for your CD.", font=("Helvetica", 18))
label_term.grid()

# Create Frame to House Dropdown + Picture
frame_options = tk.Frame(master=window_selection)
frame_options.grid(row=24, columnspan=2)

# Create Dropdown Menu
term_options = (TERM_DEFAULT, *(cd_options.keys()))
term_selection = tk.StringVar(frame_options)
term_selection.set(TERM_DEFAULT)
term_menu = tk.OptionMenu(frame_options, term_selection, *term_options)
term_menu.grid(row=1, column=1, columnspan=1, sticky='nw')

# Display Image
label_bank_graphic = tk.Label(master=frame_options, image=window_selection.images[0])
label_bank_graphic.grid(row=1, column=2, columnspan=1, sticky='e')

# Button to Navigate to Next Window
button_to_calculation = tk.Button(
    window_selection, text='Next', command=generate_validated_swapper(
        window_selection, window_calculation, validation_fun=validate_term, validation_var=term_selection
    )
)
button_to_calculation.grid(row=50, sticky='e')

# BUILD SECOND WINDOW (CALCULATION) ------------------------------------------------------------------------------------

# Left-most frame: Entry for CD principle
frame_principal = tk.Frame(window_calculation)
frame_principal.grid(row=0, column=0, columnspan=15, rowspan=50, sticky='w', padx=15, pady=5)

label_principal = tk.Label(frame_principal, text=f'Principal to\nbe invested:')
label_principal.grid(row=0, column=0, columnspan=1, sticky='w')

entry_principal = tk.Entry(frame_principal, width=10)
entry_principal.grid(row=10, column=0, columnspan=10, sticky='w')

# Right-most frame: Display for CD calculations
frame_display = tk.Frame(window_calculation)
frame_display.grid(row=0, column=50, rowspan=50, columnspan=1, sticky='e', padx=15, pady=5)

# Sub-frame for total
frame_total = tk.Frame(frame_display)
frame_display.grid(row=0, padx=5, pady=5, sticky='n')

label_total = tk.Label(frame_total, text='Total Capital at End of Term:\n')
label_total.grid(row=0, column=0, padx=5, pady=5)

display_total = tk.Label(frame_total, text=EMPTY_DISPLAY)
display_total.grid(row=5, column=0)

# Sub-frame for average dividends
frame_dividends = tk.Frame(frame_display)
frame_dividends.grid(row=50, padx=5, pady=5, sticky='s')

label_dividends = tk.Label(frame_dividends, text='Average dividends per month:\n')
label_dividends.grid(row=50, column=0, padx=5, pady=5)

display_dividends = tk.Label(frame_dividends, text=EMPTY_DISPLAY)
display_dividends.grid(row=55, column=0)

# Middle frame: Calculation button
frame_calculate = tk.Frame(window_calculation)
frame_calculate.grid(row=0, column=15, columnspan=15, rowspan=50, padx=15, pady=5)

button_to_calculate = tk.Button(
    frame_calculate, text='Calculate', command=generate_entry_calculator(
        cd_options, term_selection, entry_principal, display_dividends, display_total
    )
)
button_to_calculate.grid(row=0, column=0, sticky='n')

label_cd_graphic = tk.Label(master=frame_calculate, image=window_calculation.images[0])
label_cd_graphic.grid(row=40, column=0, sticky='s')

# Button to go back to selection window and choose a different term
button_to_selection = tk.Button(
    window_calculation, text='Back', command=generate_swapper(window_calculation, window_selection)
)
button_to_selection.grid(row=50, column=0, sticky='w')

# Button to exit
button_to_exit = tk.Button(
    window_calculation, text='Exit', command=generate_exit_program(window_selection)
)
button_to_exit.grid(row=50, column=50, sticky='e')


# Display Image
# lock_graphic = tk.PhotoImage('cd_image.png')

# RUN WINDOWS ----------------------------------------------------------------------------------------------------------
window_selection.mainloop()
