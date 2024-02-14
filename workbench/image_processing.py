import cv2
import numpy as np

from workbench.file_path_utils import PathManager


class ImageDetector:
    """
    To detect specific templates within images and computes their similarity to a reference.

    Attributes: HLS: A constant string representing the HLS color space filter. MASK_PARAM: A constant string
    indicating the key for mask parameters in TEMPLATE_DICT. OFFSET_PARAM: A constant string indicating the key for
    rectangle offset parameters in TEMPLATE_DICT. TEMPLATE_DICT: Dictionary containing detection parameters for
    various templates. Each template name maps to a sub-dictionary with keys 'HLS', 'mask_param', and 'offset_param'.

    Args: image_input (cv2.UMat): The input image data as an OpenCV UMat object. template_name (str): The name of the
    template to match, which must exist in TEMPLATE_DICT. threshold (int, optional): Specifies the maximum number of
    bounding boxes with the largest area to retain, defaults to 12.

    Methods:
        apply_hls_filter(): Applies an HLS color space filter to preprocess the image.
        find_bounding_boxes(): Identifies and selects bounding boxes that meet size criteria.
        rectangles_offset(): Adjusts the position and dimensions of bounding boxes based on template parameters.
        get_confidence_rect(): Calculates the most similar bounding box and its similarity to the specified template.
        create_masked_image(): Generates a masked version of the image using the given masking parameters.
        calculate_similarity(): Computes the similarity between two images.
    """
    HLS = 'hls'
    MASK_PARAM = 'mask_param'
    OFFSET_PARAM = 'offset_param'
    TEMPLATE_DICT = {
        'setting_button.png': {
            'hls': (
                (0, 60),
                (0, 110),
                (0, 60)
            ),
        },
        'setting_menu': {
            'hls': (
                (0, 20),
                (0, 255),
                (0, 255)
            ),
        },
        'death_Japanese.png': {
            'hls': (
                (0, 180),
                (60, 130),
                (0, 30)
            ),
            'offset_param': (0, 0, 1.0, 2.0),
        },
        'gear.png': {
            'hls': (
                (14, 20),
                (70, 200),
                (90, 200)
            ),
            'offset_param': (0.18, 0.2, 0.71, 0.71),
        },
        'gear_active.png': {
            'hls': (
                (0, 19),
                (100, 160),
                (200, 255)
            ),
            'offset_param': (0.18, 0.15, 0.78, 0.71),
        },
        'skip_button.png': {
            'hls': (
                (12, 25),
                (150, 210),
                (20, 200)
            )
        },
        'back_button.png': {
            'hls': (
                (9, 21),
                (10, 110),
                (40, 230)
            ),
            'mask_param': (
                2 / 3,
                3 / 4,
            )

        },
        'yes_button_Japanese.png': {
            'hls': (
                (12, 18),
                (100, 185),
                (30, 125)
            )
        },
        'intensity': {
            'hls': (
                (0, 30),
                (0, 255),
                (0, 255)
            ),
            'offset_param': (-0.1, -0.72, 1.18, 0.67),
        },
        'choices': {
            'hls': (
                (0, 180),
                (0, 38),
                (90, 163)
            )
        },
    }

    def __init__(self, image_input: np.ndarray, template_name: str, threshold=12):
        self.image = image_input
        self.template_name = template_name
        self.current_dict = self.TEMPLATE_DICT[self.template_name]
        self.rectangles_list = []
        self.threshold = threshold

    def apply_hls_filter(self, image):
        h_range, l_range, s_range = self.current_dict[self.HLS]
        h_channel, l_channel, s_channel = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HLS))
        h_mask = cv2.inRange(h_channel, h_range[0], h_range[1])
        l_mask = cv2.inRange(l_channel, l_range[0], l_range[1])
        s_mask = cv2.inRange(s_channel, s_range[0], s_range[1])

        mask = cv2.bitwise_and(h_mask, cv2.bitwise_and(s_mask, l_mask))
        # mask = cv2.bitwise_and(
        #     cv2.inRange(hls_channels[0], *h_range),
        #     cv2.inRange(hls_channels[1], *l_range),
        #     cv2.inRange(hls_channels[2], *s_range)
        # )
        return cv2.bitwise_and(image, image, mask=mask)

    def find_bounding_boxes(self):
        self.rectangles_list.clear()
        image_filtered = self.apply_hls_filter(self.image)

        # _, image_binary = cv2.threshold(cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY), 128, 255, cv2.THRESH_BINARY)
        _, image_binary = cv2.threshold(cv2.cvtColor(image_filtered, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_OTSU)
        # cv2.imwrite('1.png', image_binary)
        # cv2.imshow('1', image_filtered)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        contours, _ = cv2.findContours(image_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        bounding_rects = [cv2.boundingRect(c) for c in contours]
        # apply offset
        bounding_rects = self.rectangles_offset(bounding_rects)
        sizes = [rect[2] * rect[3] for rect in bounding_rects]
        sizes = sorted(sizes, reverse=True)

        threshold_size = sizes[min(self.threshold - 1, len(sizes) - 1)]
        self.rectangles_list.extend(
            rect for rect in bounding_rects
            if rect[2] * rect[3] >= threshold_size and 0.1 <= rect[2] / rect[3] <= 10
        )

        # i = 1000
        for rect in self.rectangles_list:
            x, y, w, h = rect
            # print(rect)
            roi = self.image[y:y + h, x:x + w]

            cv2.imshow('1', roi)
            cv2.waitKey(0)
        # cv2.imwrite(f'{i}.png', roi)
        # i += 1

        return self.rectangles_list

    def rectangles_offset(self, rectangles_list):
        offset_factors = self.current_dict.get(self.OFFSET_PARAM, [0, 0, 1, 1])
        # print(f'offsets:{offset_factors}')
        x_offset_factor, y_offset_factor, width_scale_factor, height_scale_factor = offset_factors

        image_width, image_height = self.image.shape[1], self.image.shape[0]

        rectangles_offset_list = [(max(0, round(x + w * x_offset_factor)),  # 确保x坐标不小于0
                                   max(0, round(y + h * y_offset_factor)),  # 确保y坐标不小于0
                                   max(1, min(image_width, round(w * width_scale_factor))),  # 确保宽度不超过图像宽度
                                   max(1, min(image_height, round(h * height_scale_factor))))  # 确保高度不超过图像高度
                                  for x, y, w, h in rectangles_list]

        return rectangles_offset_list

    def get_confidence_rect(self):

        # Detect rectangles and draw them on the image
        self.find_bounding_boxes()

        # Load the skip button template
        template = cv2.imread(PathManager.get_local_image(self.template_name))
        # template = self.apply_hls_filter(template)
        # cv2.imshow('1', template)
        # cv2.waitKey(0)
        # template = cv2.imread(get_local_image('skip_button.png'))

        # Initialize maximum similarity and corresponding rectangle
        max_similarity = 0
        max_similarity_rect = None

        # Calculate similarity for each rectangle
        mask_param_list = self.current_dict.get(self.MASK_PARAM, [])
        template_masked = self.create_masked_image(template, *mask_param_list)
        for rect in self.rectangles_list:
            x, y, w, h = rect
            # print(rect)
            roi = self.image[y:y + h, x:x + w]
            # roi = self.apply_hls_filter(roi)
            roi_masked = self.create_masked_image(roi, *mask_param_list)
            # cv2.imshow('1', roi)
            # cv2.waitKey(0)
            similarity = self.calculate_similarity(roi_masked, template_masked)

            # Update max similarity and max similarity rectangle if necessary
            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_rect = rect

            # cv2.imshow("12", roi)
            # cv2.waitKey(0)
            # print(f"Similarity for rectangle at ({x}, {y}) is {similarity:.4f}")

        # Return max similarity and it's corresponding rectangle
        return max_similarity, max_similarity_rect

    @staticmethod
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

    @staticmethod
    def calculate_similarity(image, template: cv2.typing.MatLike):
        # 调整图片大小
        target_size = (template.shape[1], template.shape[0])
        image = cv2.resize(image, target_size)
        mask = cv2.inRange(image, np.array([0, 0, 0]), np.array([255, 255, 255]))
        # 创建ORB特征提取器
        orb = cv2.ORB.create(edgeThreshold=0)

        # 从两幅图像中查找关键点和描述符
        # cv2.imshow('1', image)
        # cv2.waitKey(0)
        try:
            kp1, des1 = orb.detectAndCompute(image, mask)
        except cv2.error:
            # cv2.imshow('1', image)
            # cv2.waitKey(0)
            return 0
        kp2, des2 = orb.detectAndCompute(template, mask)

        # 创建Brute Force Matcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)  # 修改为False，以便返回两个最近的匹配点

        # 使用Matcher匹配描述符
        matches = bf.knnMatch(des1, des2, k=2)  # 修改为knnMatch，以便返回两个最近的匹配点

        # 应用比例测试，过滤掉明显不匹配的点
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:  # 如果第一个匹配点的距离小于第二个匹配点的距离的0.75倍，那么它是好的匹配点
                good_matches.append(m)

        # 根据好的匹配数返回相似度
        return len(good_matches)

# if __name__ == "__main__":
#     def main():
#         image_path = 'back_button.png'  # Replace with your image path
#         create_masked_image(image_path, height_factor=2 / 3, width_factor=3 / 4, preserve_center=True)
#
#
#     main()
