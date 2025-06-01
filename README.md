# EyeQ-Test

EyeQ-Test is a UI showcase project demonstrating different user interface components and designs using Python’s Tkinter library, enhanced with ttkbootstrap for modern theming.  
This repository serves as a reference for UI best practices, visual experimentation, and rapid prototyping.

![image](https://github.com/user-attachments/assets/84961442-4c6a-4875-b47a-ab897c2b2baa)

## Features

- Collection of UI components for demonstration and learning
- Modular and easy to extend with new designs
- Built to highlight modern interface patterns
- Modern theming with [ttkbootstrap](https://ttkbootstrap.readthedocs.io/) for Tkinter

## UI Library & Themes

This project uses:
- **Tkinter:** Python’s standard GUI library for building user interfaces.
- **ttkbootstrap:** A theming library for Tkinter that provides modern, Bootstrap-inspired UI themes.

### Available Themes

You can choose from many built-in light and dark themes in ttkbootstrap. Popular options include:

**Light Themes:**
- flatly
- journal
- litera
- lumen
- minty
- morph
- pulse
- sandstone
- united
- yeti
- cosmo
- simplex

**Dark Themes:**
- darkly
- cyborg
- solar
- superhero
- vapor
- minty-dark

See the [official ttkbootstrap documentation](https://ttkbootstrap.readthedocs.io/en/latest/themes/) for previews and the full list.

You can change the project theme by Editing :
```
 super().__init__(themename='cyborg')
```
located at line 18.

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Kebabist/EyeQ-Test.git
    cd EyeQ-Test
    ```

2. **Install dependencies**  
    This project requires Python and the `ttkbootstrap` package:
    ```bash
    pip install ttkbootstrap
    ```

3. **Run the project**  
    *(Provide run commands or entry points, e.g., `python main.py`)*

## Project Structure

- `src/` — source code and UI components
- `assets/` — images, icons, and styles
- `README.md` — project overview

## License

This project is licensed under the [GNU GPL v3.0](https://choosealicense.com/licenses/gpl-3.0/).
