import cv2
import numpy as np
import tkinter as tk
# import customtkinter
from tkinter import filedialog
from tkinter import messagebox


def detect_dot_and_save_coordinates(image_path):
    # Step 2: Process the image to detect the dot or point
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use a simple threshold to detect the point (assuming it's a dark point on a light background)
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the largest contour is the point (this may need to be adjusted based on your image)
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the coordinates of the center of the contour
    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    # Step 3: Extract the coordinates
    coordinates = (cX, cY)

    # Step 4: Save the coordinates to a file
    with open('coordinates.txt', 'w') as file:
        file.write(f'Point coordinates: {coordinates}\n')

    # Optional: Display the image with the detected point
    cv2.circle(image, coordinates, 5, (0, 0, 255), -1)
    cv2.imshow('Detected Point', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return coordinates

def upload_and_process_image():
    # Open a file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    
    if file_path:
        # Detect dot and save coordinates
        try:
            coordinates = detect_dot_and_save_coordinates(file_path)
            messagebox.showinfo("Success", f"Coordinates saved to 'coordinates.txt': {coordinates}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main application window
app = tk.Tk()
app.title("Dot Detector")
app.geometry("500x400")



# Create and place a button to upload and process the image
upload_button = tk.Button(app, text="Upload Image", command=upload_and_process_image)
upload_button.pack(expand=True)

# Run the application
app.mainloop()
