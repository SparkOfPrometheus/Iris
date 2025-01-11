# Iris


Iris is a minimalist whiteboard application using Python and PyQt5.

## Features

- **Customizable Brush Sizes and Colors**: Choose from a palette of 12 colors and adjust brush size between 1 and 13 pixels.
- **Eraser and Marker Modes**: Switch between drawing and erasing with ease.
- **Clear Canvas and Save Functionality**: Clear the entire canvas or save your drawing as a PNG image.
- **Responsive and Intuitive UI**: User-friendly interface with a clean design.

## Installation

### Prerequisites

Ensure you have the following installed on your Windows machine:

- **Python 3.7+**: [Download Python](https://www.python.org/downloads/)
- **pip**: Comes bundled with Python. Verify by running `pip --version` in your command prompt.

### Dependencies

Install the required Python packages using pip:
bash
pip install PyQt5 Pillow

### Project Structure
css
Copy code
Iris/
├── assets/
│   ├── cursor.png
│   ├── sand2.jpg
│   └── whiteboardpaper.jpg
├── src/
│   └── Iris.py
├── LICENSE
└── README.md
assets/: Contains image assets used in the application.
src/: Contains the main application code.
LICENSE: GPLv3 license text.
README.md: Project documentation.
Assets Preparation
Ensure the following assets are placed in the assets folder:

cursor.png: Custom cursor image.
sand2.jpg: Background image for the application.
whiteboardpaper.jpg: Background image for the canvas.
You can use your own images or download suitable placeholders.

Usage
Navigate to the Project Directory:

Open your command prompt and navigate to the Iris project directory.

bash
Copy code
cd path\to\Iris\src
Run the Application:

Execute the Iris.py script using Python.

bash
Copy code
python Iris.py
The Iris whiteboard application should launch, displaying the toolbar and the canvas.

License
This project is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

Dependencies
PyQt5 - Python bindings for the Qt application framework. Licensed under GPLv3.
Pillow - Python Imaging Library (PIL) Fork. Licensed under the PIL Software License.
Packaging the Application (Optional)
To distribute Iris as a standalone Windows executable, you can use PyInstaller.

Install PyInstaller:

bash
Copy code
pip install pyinstaller
Create the Executable:

bash
Copy code
pyinstaller --onefile --windowed src/Iris.py
This command generates a dist folder containing the Iris.exe executable.

Include Assets:

To ensure the assets folder is included, use the --add-data option.

bash
Copy code
pyinstaller --onefile --windowed --add-data "assets;assets" src/Iris.py
Run the Executable:

Navigate to the dist folder and run Iris.exe.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.

## 4. Additional Notes

### Project Structure

Ensure your project directory follows this structure to maintain organization and compliance:

Iris/ ├── assets/ │ ├── cursor.png │ ├── sand2.jpg │ └── whiteboardpaper.jpg ├── src/ │ └── Iris.py ├── LICENSE └── README.md

arduino
Copy code

- **assets/**: Store all image assets here. Ensure that you have the rights to use and distribute these images, especially since GPLv3 requires that all parts of the project are compatible with its terms.
- **src/**: Contains the main Python application code.
- **LICENSE**: Full text of GPLv3.
- **README.md**: Documentation and project overview, including licensing information.

### Compliance Checklist

To ensure full compliance with GPLv3, verify the following:

1. **LICENSE File**: Present in the root directory with the complete GPLv3 text.
2. **License Headers**: Each source code file (e.g., `Iris.py`) includes a GPLv3 license header at the top.
3. **Source Code Availability**: If distributing binaries, ensure that the corresponding source code is available.
4. **Dependencies**: All dependencies are compatible with GPLv3.
5. **Asset Licensing**: All assets used are either created by you or have licenses compatible with GPLv3.











