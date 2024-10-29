import cv2
import numpy as np
from weather_api import WeatherDataCollector

collector = WeatherDataCollector()
city = "Singapore"
print(f"\nFetching weather data for {city}...")
weather_data = collector.get_weather_data(city)
# Interpret rain_chance & uv_index in range [0, 1]
rain_chance, uv_index = collector.process_weather_metrics(weather_data)

from path_finding import PathFinder

map_image = cv2.imread("NTU_minimap.png")
from map import positions, connections
finder = PathFinder(positions, connections)

vis_map = finder.visualize(map_image)
cv2.imshow(f"Path Visualization", vis_map)

# Global variables for toggle states
show_color = True
enable_sliders = True


def on_trackbar(val):
    # This function will be called when the trackbar value changes
    pass


def toggle_color(val):
    global show_color
    show_color = bool(val)


def toggle_sliders(val):
    global enable_sliders
    enable_sliders = bool(val)

    # Enable/disable all sliders based on toggle state
    if enable_sliders:
        cv2.setTrackbarPos('R', 'Control Panel', cv2.getTrackbarPos('R', 'Control Panel'))
    else:
        # Store current values before disabling
        r = cv2.getTrackbarPos('R', 'Control Panel')
        g = cv2.getTrackbarPos('G', 'Control Panel')
        b = cv2.getTrackbarPos('B', 'Control Panel')
        # Set all sliders to 0 when disabled
        cv2.setTrackbarPos('R', 'Control Panel', 0)
        cv2.setTrackbarPos('G', 'Control Panel', 0)
        cv2.setTrackbarPos('B', 'Control Panel', 0)


# Create a black image and windows
img = np.zeros((300, 512, 3), np.uint8)
cv2.namedWindow('Display Window')
cv2.namedWindow('Control Panel')

# Create trackbars for color change
cv2.createTrackbar('R', 'Control Panel', 0, 255, on_trackbar)
cv2.createTrackbar('G', 'Control Panel', 0, 255, on_trackbar)
cv2.createTrackbar('B', 'Control Panel', 0, 255, on_trackbar)

# Create toggle buttons (implemented as trackbars with max value 1)
cv2.createTrackbar('Show Color', 'Control Panel', 1, 1, toggle_color)
cv2.createTrackbar('Enable Sliders', 'Control Panel', 1, 1, toggle_sliders)

while True:
    # Create a copy of the base image
    display_img = img.copy()

    if enable_sliders:
        # Get current positions of trackbars
        r = cv2.getTrackbarPos('R', 'Control Panel')
        g = cv2.getTrackbarPos('G', 'Control Panel')
        b = cv2.getTrackbarPos('B', 'Control Panel')
    else:
        r, g, b = 0, 0, 0

    if show_color:
        # Update image color based on trackbar positions
        display_img[:] = [b, g, r]  # OpenCV uses BGR format
    else:
        # Show black screen when color is toggled off
        display_img[:] = [0, 0, 0]

    # Add text to show current RGB values
    text = f'RGB: ({r}, {g}, {b})'
    cv2.putText(display_img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255 - b, 255 - g, 255 - r), 2)

    # Display the image
    cv2.imshow('Display Window', display_img)
    cv2.imshow('Control Panel', np.zeros((100, 512, 3), np.uint8))  # Control panel background

    # Break the loop when 'ESC' is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()