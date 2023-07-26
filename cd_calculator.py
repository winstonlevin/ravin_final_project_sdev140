from typing import Optional, Union, Callable
import tkinter as tk

# CONSTANTS ------------------------------------------------------------------------------------------------------------
DAYS_PER_YEAR = 365.
MONTHS_PER_YEAR = 12
TERM_DEFAULT = '[Select a Term]'
TKINTER_WINDOW = Union[tk.Tk, tk.Toplevel]


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


def calculate_cd(principle: float, rate: float, term: float) -> (float, float):
    """
    This function returns average monthly dividend and total amount at end of term.

    :param principle: float, the starting capital, dollars
    :param rate: float, the annual interest rate, fraction
    :param term: float, the term, months
    :return: (float, float), a Tuple of the mean monthly return and total at end of term
    """

    total = principle * (1 + rate / DAYS_PER_YEAR) ** (term * DAYS_PER_YEAR / MONTHS_PER_YEAR)
    mean_return = (total - principle) / term

    return mean_return, total


# DEFINE WINDOW CLASS --------------------------------------------------------------------------------------------------
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

window_calculation = Window(window_selection, title='Calculate CD Gains', images=['cd_image.png'])
window_calculation.withdraw()  # Not open by default

# BUILD FIRST WINDOW (TERM SELECTION) ----------------------------------------------------------------------------------
window_selection.resizable(width=True, height=True)

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
button_to_selection = tk.Button(
    window_calculation, text='Back', command=generate_swapper(window_calculation, window_selection)
)
button_to_selection.grid()


# Display Image
# lock_graphic = tk.PhotoImage('cd_image.png')

# RUN WINDOWS ----------------------------------------------------------------------------------------------------------
window_selection.mainloop()
