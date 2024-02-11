import cv2
import numpy as np


class ImageDetector:
    def __init__(self, image_input: cv2.UMat, template_name: str):
        self.image = image_input
        self.template_name = template_name

    def get_confidence_rect(self):
        template_dict_current: dict = template_dict[self.template_name]
        # Load and pre-process the image
        image_filtered = apply_hsl_filter(
            self.image,
            *template_dict_current[hsl]
        )
        # _, image_binary = cv2.threshold(cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY)
        _, image_binary = cv2.threshold(cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_OTSU)

        # Detect rectangles and draw them on the image
        rectangles = find_bounding_boxes(image_binary, 12)
        offset_factors = template_dict_current.get(offset_param, [])
        rectangles_offset = image_processing.rectangles_offset(rectangles, *offset_factors)

        # Load the skip button template
        template = cv2.imread(file_path_utils.get_local_image(self.template_name))
        # cv2.imshow('1', template)
        # cv2.waitKey(0)
        # template = cv2.imread(get_local_image('skip_button.png'))

        # Initialize maximum similarity and corresponding rectangle
        max_similarity = 0
        max_similarity_rect = None

        # Calculate similarity for each rectangle
        mask_param_list = template_dict_current.get(mask_param, [])
        template_masked = image_processing.create_masked_image(template, *mask_param_list)
        for rect in rectangles_offset:
            x, y, w, h = rect
            roi = self.image[y:y + h, x:x + w]
            roi_masked = image_processing.create_masked_image(roi, *mask_param_list)
            # cv2.imshow('1', roi_masked)
            # cv2.waitKey(0)
            similarity = calculate_similarity(roi_masked, template_masked)

            # Update max similarity and max similarity rectangle if necessary
            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_rect = rect

            # cv2.imshow("12", roi)
            # cv2.waitKey(0)
            # print(f"Similarity for rectangle at ({x}, {y}) is {similarity:.4f}")

        # Return max similarity and it's corresponding rectangle
        return max_similarity, max_similarity_rect


# Define the scaling factor as constants
SCALING_FACTOR_HEIGHT = 2 / 3
SCALING_FACTOR_WIDTH = 3 / 4


def rectangles_offset(rectangles, x_offset_factor=0, y_offset_factor=0, width_scale_factor=1,
                      height_scale_factor=1):
    rectangles_list = []
    for rect in rectangles:
        x, y, w, h = rect
        rectangles_list.append((round(x + w * x_offset_factor), round(y + h * y_offset_factor),
                                round(w * width_scale_factor), round(h * height_scale_factor)))

    return rectangles_list


def create_masked_image(image, height_factor=None, width_factor=None, preserve_center=False):
    if height_factor is None or width_factor is None:
        return image
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
    # cv2.imshow('Processed Image', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return result


if __name__ == "__main__":
    def main():
        image_path = 'back_button.png'  # Replace with your image path
        create_masked_image(image_path, height_factor=2 / 3, width_factor=3 / 4, preserve_center=True)


    main()
