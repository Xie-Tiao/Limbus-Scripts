import cv2
import numpy as np

# Define the scaling factor as constants
SCALING_FACTOR_HEIGHT = 2 / 3
SCALING_FACTOR_WIDTH = 3 / 4
IMAGE_NAME = 'back_button.png'


def create_masked_image(image_path, height_factor, width_factor, preserve_center=False):
    # Load the image
    image = cv2.imread(image_path)

    # Obtain the image dimensions
    h, w, channels = image.shape

    # Create a white image of the same dimensions
    mask = np.zeros((h, w, channels), np.uint8) if preserve_center else np.ones((h, w, channels), np.uint8) * 255

    # Define your rectangle
    start_y, start_x = int(h * (1 - height_factor) / 2), int(w * (1 - width_factor) / 2)
    end_y, end_x = int(h * (1 + height_factor) / 2), int(w * (1 + width_factor) / 2)

    # Set rectangle color based on preserve_center
    rectangle_color = (255, 255, 255) if preserve_center else (0, 0, 0)

    # Draw a rectangle on the white mask
    cv2.rectangle(mask, (start_x, start_y), (end_x, end_y), rectangle_color, -1)

    # Combine the image with the mask
    result = cv2.bitwise_and(image, mask)

    # Use cv2.imshow() function to display the image
    # cv2.imwrite(IMAGE_NAME, result)
    cv2.imshow('Processed Image', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    image_path = IMAGE_NAME  # Replace with your image path
    create_masked_image(image_path, height_factor=SCALING_FACTOR_HEIGHT, width_factor=SCALING_FACTOR_WIDTH,
                        preserve_center=False)


if __name__ == "__main__":
    main()
