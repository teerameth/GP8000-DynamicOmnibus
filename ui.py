import cv2
import numpy as np


class WeatherControlPanel:
    def __init__(self):
        # Window setup
        self.window_name = "Weather Controls"
        self.width = 600
        self.height = 400
        self.img = np.ones((self.height, self.width, 3), dtype=np.uint8) * 240

        # Control states
        self.mode = False  # False: Manual, True: Weather API
        self.avoid_road = False
        self.avoid_sun = False
        self.avoid_rain = False
        self.uv_index = 0
        self.rain_chance = 0

        # Button dimensions
        self.btn_width = 200
        self.btn_height = 40
        self.spacing = 20

        cv2.namedWindow(self.window_name)

        # Create trackbars
        cv2.createTrackbar("UV Index", self.window_name, 0, 3, self.on_uv_change)
        cv2.createTrackbar("Rain Chance", self.window_name, 0, 100, self.on_rain_change)

        # Mouse callback
        cv2.setMouseCallback(self.window_name, self.handle_click)

    def on_uv_change(self, value):
        self.uv_index = value
        self.draw()

    def on_rain_change(self, value):
        self.rain_chance = value / 100.0
        self.draw()

    def get_uv_text(self):
        uv_levels = ["Low", "Intermediate", "High", "Extreme"]
        return uv_levels[self.uv_index]

    def draw_button(self, y, text, state):
        x = 20
        cv2.rectangle(self.img, (x, y), (x + self.btn_width, y + self.btn_height),
                      (120, 120, 120) if state else (200, 200, 200), -1)
        cv2.rectangle(self.img, (x, y), (x + self.btn_width, y + self.btn_height),
                      (100, 100, 100), 1)

        # Add text
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0]
        text_x = x + (self.btn_width - text_size[0]) // 2
        text_y = y + (self.btn_height + text_size[1]) // 2
        cv2.putText(self.img, text, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    def draw(self):
        # Clear background
        self.img.fill(240)

        # Draw toggle buttons
        self.draw_button(20, f"Mode: {'Weather API' if self.mode else 'Manual'}", self.mode)
        self.draw_button(80, f"Avoid Road: {'On' if self.avoid_road else 'Off'}", self.avoid_road)
        self.draw_button(140, f"Avoid Sun: {'On' if self.avoid_sun else 'Off'}", self.avoid_sun)
        self.draw_button(200, f"Avoid Rain: {'On' if self.avoid_rain else 'Off'}", self.avoid_rain)

        # Draw slider values
        cv2.putText(self.img, f"UV Index: {self.get_uv_text()}", (250, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        cv2.putText(self.img, f"Rain Chance: {self.rain_chance:.2%}", (250, 320),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

        cv2.imshow(self.window_name, self.img)

    def handle_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check if click is within any button area
            if 20 <= x <= 20 + self.btn_width:
                if 20 <= y <= 20 + self.btn_height:
                    self.mode = not self.mode
                elif 80 <= y <= 80 + self.btn_height:
                    self.avoid_road = not self.avoid_road
                elif 140 <= y <= 140 + self.btn_height:
                    self.avoid_sun = not self.avoid_sun
                elif 200 <= y <= 200 + self.btn_height:
                    self.avoid_rain = not self.avoid_rain
                self.draw()

    def run(self):
        self.draw()
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break

        cv2.destroyAllWindows()

        # Return final states
        return {
            'mode': 'Weather API' if self.mode else 'Manual',
            'avoid_road': self.avoid_road,
            'avoid_sun': self.avoid_sun,
            'avoid_rain': self.avoid_rain,
            'uv_index': self.get_uv_text(),
            'rain_chance': self.rain_chance
        }


if __name__ == "__main__":
    control_panel = WeatherControlPanel()
    final_states = control_panel.run()
    print("Final states:", final_states)