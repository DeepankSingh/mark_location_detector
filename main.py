from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.image import Image as CoreImage
from kivy.utils import platform
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
import cv2
import numpy as np
from PIL import Image as PILImage
import os
import io

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        self.label = Label(
            text="Upload an image with a mark on a human body",
            font_size='20sp',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        layout.add_widget(self.label)

        self.upload_button = Button(
            text="Upload Image",
            font_size='18sp',
            size_hint=(0.5, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.8}
        )
        self.upload_button.bind(on_press=self.show_file_chooser)
        layout.add_widget(self.upload_button)

        self.image_display = Image(
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.4}
        )
        layout.add_widget(self.image_display)

        self.result_label = Label(
            text="Mark location will appear here",
            font_size='18sp',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'bottom': 0.05}
        )
        layout.add_widget(self.result_label)

        self.add_widget(layout)

    def show_file_chooser(self, instance):
        content = FileChooserIconView()
        content.bind(on_submit=self.load_image)
        self.popup = Popup(title="Choose an image", content=content, size_hint=(1, 1))
        self.popup.open()

    def load_image(self, filechooser, selection, touch):
        self.popup.dismiss()
        if selection:
            file_path = selection[0]
            self.process_image(file_path)

    def process_image(self, image_path):
        try:
            img_pil = PILImage.open(image_path)
            img_pil_resized = img_pil.resize((400, 404))
            img_cv = cv2.cvtColor(np.array(img_pil_resized), cv2.COLOR_RGB2BGR)
            mark_location = self.identify_mark(img_cv)

            if mark_location is None:
                self.show_popup("No Mark Found", "No mark was detected on the image.")
                return

            cv2.circle(img_cv, mark_location, 5, (0, 255, 0), -1)
            img_with_mark_pil = PILImage.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
            buf = io.BytesIO()
            img_with_mark_pil.save(buf, format='png')
            buf.seek(0)
            texture = CoreImage(buf, ext='png').texture
            self.image_display.texture = texture
            self.result_label.text = f"Mark location: ({mark_location[0]}, {mark_location[1]})"
            self.write_coordinates_to_file(image_path, mark_location)

        except FileNotFoundError:
            self.show_popup("Error", "File not found. Please select a valid image file.")
        except Exception as e:
            self.show_popup("Error", f"Error processing image: {e}")

    def identify_mark(self, img):
        try:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_color = np.array([0, 50, 50])
            upper_color = np.array([179, 255, 255])
            mask = cv2.inRange(hsv, lower_color, upper_color)
            res = cv2.bitwise_and(img, img, mask=mask)
            gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (3, 3), 0)
            thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                contours = [contour for contour in contours if cv2.contourArea(contour) > 10]
                if contours:
                    largest_contour = max(contours, key=cv2.contourArea)
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        return (cx, cy)
            return None

        except Exception as e:
            self.show_popup("Error", f"Error identifying mark: {e}")
            return None

    def write_coordinates_to_file(self, image_path, coordinates):
        try:
            if platform == 'android':
                from android.storage import primary_external_storage_path
                directory = os.path.join(primary_external_storage_path(), 'MarkDetecter')
            else:
                directory = os.path.join(os.path.expanduser("~"), 'MarkDetecter')

            if not os.path.exists(directory):
                os.makedirs(directory)

            file_path = os.path.join(directory, 'coordinates.txt')

            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    lines = file.readlines()
            else:
                lines = []

            image_name = os.path.basename(image_path)
            new_line = f"{image_name}: ({coordinates[0]}, {coordinates[1]})\n"
            updated = False
            for i, line in enumerate(lines):
                if line.startswith(image_name):
                    if line.strip() != new_line.strip():
                        lines[i] = new_line
                        updated = True
                    break
            else:
                lines.append(new_line)

            with open(file_path, "w") as file:
                file.writelines(lines)

            if updated:
                self.show_popup("File Updated", f"Coordinates updated in {file_path}")
            else:
                self.show_popup("File Saved", f"Coordinates saved to {file_path}")

        except Exception as e:
            self.show_popup("Error", f"Error saving coordinates: {e}")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, size_hint_y=None, height=50))
        button = Button(text="OK", size_hint_y=None, height=50)
        content.add_widget(button)

        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        button.bind(on_press=popup.dismiss)
        popup.open()

    def calculate_text_height(self, text, width=380, font_size=14):
        label = Label(text=text, font_size=font_size, text_size=(dp(width), None))
        label.texture_update()
        return label.texture_size[1]

class MarkIdentificationApp(App):
    def build(self):
        return HomeScreen()

if __name__ == '__main__':
    MarkIdentificationApp().run()
