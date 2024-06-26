# mark_location_detector


This repo contains Summer pet project:  Mark Location Detector


# Mark Detection App

## Overview

The Mark Detection App is a Kivy-based application designed to upload, process, and identify marks on images of human bodies. It utilizes image processing techniques with OpenCV and Pillow (PIL) to detect and highlight specific marks on the uploaded images. The app also saves the coordinates of the detected marks to a text file for future reference.

## Features

- **User Interface**: Simple and intuitive interface using Kivy.
- **File Chooser**: Allows users to select an image from their device.
- **Image Processing**: Detects and highlights marks on the image using OpenCV.
- **Coordinates Saving**: Saves the coordinates of detected marks to a text file.
- **Cross-Platform**: Works on Android and other operating systems.

## Requirements

- Python 3.x
- Kivy
- OpenCV
- Pillow (PIL)
- NumPy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DeepankSingh/mark-detection-app.git
   cd mark-detection-app
   ```

2. Install the required dependencies:
   ```bash
   pip install kivy opencv-python pillow numpy
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. In the application:
   - Click on the "Upload Image" button to open the file chooser dialog.
   - Select an image file with a mark on a human body.
   - The app will process the image, detect the mark, and display the image with the mark highlighted.
   - The coordinates of the detected mark will be displayed and saved to a text file.

## Project Structure

```
mark-detection-app/
│
├── main.py                # Main application script
├── README.md              # Project readme file
└── Images/                # Folder for images
```

## Code Explanation

### UI Design

- **FloatLayout**: Used for flexible positioning of UI elements.
- **Labels and Buttons**: For displaying text and interactive elements.
- **FileChooserIconView**: To allow users to select image files.
- **Popup**: To show messages and feedback to users.

### Image Processing

- **Pillow (PIL)**: For loading and resizing images.
- **OpenCV**: For image processing and mark detection.
- **NumPy**: For array manipulation and image data handling.

### Key Methods

- `show_file_chooser(self, instance)`: Opens the file chooser dialog.
- `load_image(self, filechooser, selection, touch)`: Loads the selected image.
- `process_image(self, image_path)`: Processes the image to identify and highlight the mark.
- `identify_mark(self, img)`: Identifies the mark on the image using contour detection.
- `write_coordinates_to_file(self, image_path, coordinates)`: Writes the coordinates of the detected mark to a text file.
- `show_popup(self, title, message)`: Displays a popup message to the user.

## Use Case

### Scenario

A dermatologist wants to document the location of specific marks on patients' bodies for medical records. The Mark Detection App allows the dermatologist to:

1. Upload images of the patient's body.
2. Automatically detect and highlight the marks.
3. Save the coordinates of the marks for future reference.

### Benefits

- **Efficiency**: Automates the process of identifying and documenting marks.
- **Accuracy**: Provides precise coordinates of detected marks.
- **Usability**: Easy to use with a straightforward interface.

## Future Improvements

- **Enhance Detection Algorithm**: Improve the accuracy of mark detection with more advanced image processing techniques.
- **Multiple Marks Detection**: Extend the functionality to detect multiple marks in a single image.
- **User Annotations**: Allow users to manually annotate and adjust detected marks.
- **Database Integration**: Store images and coordinates in a database for better record management.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---
