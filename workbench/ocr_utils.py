import json
import os

from rapidocr_onnxruntime import RapidOCR
from thefuzz import process, fuzz

from workbench.file_path_utils import PathManager
from workbench.read_settings import SettingsReader


class Ocr:
    """
    To recognize text in images using the RapidOCR library.

    This class provides a language-aware OCR engine initialization and text recognition functionality.
    Depending on the current language settings, it loads the appropriate model for Japanese or Korean text recognition.
    For other languages, it initializes the OCR engine with default parameters.

    Attributes:
        _model_path_japanese (str): Relative path to the Japanese OCR model file.
        _model_path_korean (str): Relative path to the Korean OCR model file.
        _choices_path (str): Relative path to the choices dictionary JSON file.
        _current_language (str): The currently set language for OCR processing.
        _ocr_engine (RapidOCR or None): An instance of the RapidOCR class, initialized based on the current language.
        _choices (list): A list of choices for the current language.

    Methods: set_language(cls, language): Sets the current language for OCR processing. init_orc_engine(cls):
    Initializes the OCR engine according to the current language setting. get_orc_engine(cls): Retrieves the current
    OCR engine instance, initializing if necessary due to a language change. recognize_text(cls, image,
    use_det=False, use_cls=False, use_rec=True): Recognizes text in an image and returns the result.
    """
    _model_path_japanese = os.path.join(PathManager.MODEL_RELPATH, 'japan_PP-OCRv3_rec_infer.onnx')
    _model_path_korean = os.path.join(PathManager.MODEL_RELPATH, 'korean_PP-OCRv3_rec_infer.onnx')
    _choices_path = os.path.join(PathManager.ASSETS_RELPATH, 'choices_dict.json')
    _current_language = None
    # 调用init_orc_engine
    _ocr_engine = None
    _choices = []
    with open(_choices_path, 'r', encoding='utf-8') as f:
        _choices_dict = json.load(f)

    def __init__(self, language):
        if language == 'Japanese':
            self.ocr_engine = RapidOCR(
                rec_model_path=self._model_path_japanese,
            )
        elif language == 'Korean':
            self.ocr_engine = RapidOCR(
                rec_model_path=self._model_path_korean,
            )
        else:
            self.ocr_engine = RapidOCR()

    def check_text_in_rectangles(self, image, rectangles_list, target: str, use_det=False, use_cls=False, use_rec=True):
        matched_str = ''
        best_rect = None
        max_score = -1
        for rect in rectangles_list:
            x, y, w, h = rect
            roi = image[y:y + h, x:x + w]
            try:
                result_list, _ = self.recognize_text_instance(roi, use_det=use_det, use_cls=use_cls, use_rec=use_rec)
            except ValueError:
                result_list = self.recognize_text_instance(roi, use_det=use_det, use_cls=use_cls, use_rec=use_rec)
            result_str = result_list[0][0] if result_list else None
            # 现在使用限定长度差异的choices进行匹配
            score = fuzz.ratio(target, result_str)

            # 更新最佳匹配结果
            if score > max_score:
                max_score = score
                matched_str = result_str
                best_rect = rect

        return matched_str, best_rect, max_score

    @classmethod
    def check_text_in_rectangles_cls(cls, image, rectangles_list, target: str, use_det=False, use_cls=False,
                                     use_rec=True):
        matched_str = ''
        best_rect = None
        max_score = -1
        for rect in rectangles_list:
            x, y, w, h = rect
            roi = image[y:y + h, x:x + w]
            try:
                result_list, _ = cls.recognize_text(roi, use_det=use_det, use_cls=use_cls, use_rec=use_rec)
            except ValueError:
                result_list = cls.recognize_text(roi, use_det=use_det, use_cls=use_cls, use_rec=use_rec)
            result_str = result_list[0][0] if result_list else None
            print(result_str)
            # 现在使用限定长度差异的choices进行匹配
            score = fuzz.ratio(target, result_str)

            # 更新最佳匹配结果
            if score > max_score:
                max_score = score
                matched_str = result_str
                best_rect = rect

        return matched_str, best_rect, max_score

    @classmethod
    def init_orc_engine(cls):
        if cls._current_language == 'Japanese':
            ocr_engine = RapidOCR(
                rec_model_path=cls._model_path_japanese,
            )
        elif cls._current_language == 'Korean':
            ocr_engine = RapidOCR(
                rec_model_path=cls._model_path_korean,
            )
        else:
            ocr_engine = RapidOCR()

        return ocr_engine

    @classmethod
    def get_orc_engine(cls):
        current_language = SettingsReader.read_option('Language', 'current')
        if current_language != cls._current_language:
            cls._current_language = current_language
            cls._choices = cls._choices_dict[current_language]
            cls._ocr_engine = cls.init_orc_engine()

        return cls._ocr_engine

    @classmethod
    def recognize_text(cls, image, use_det=False, use_cls=False, use_rec=True):
        ocr_engine = cls.get_orc_engine()
        result, _ = ocr_engine(image, use_det=use_det, use_cls=use_cls, use_rec=use_rec)
        return result

    def recognize_text_instance(self, image, use_det=False, use_cls=False, use_rec=True):
        result, _ = self.ocr_engine(image, use_det=use_det, use_cls=use_cls, use_rec=use_rec)
        return result

    @classmethod
    def recognize_rectangles(cls, image, rectangles_list, use_det=False, use_cls=False, use_rec=True):
        text_rect_list = []
        for rect in rectangles_list:
            x, y, w, h = rect
            roi = image[y:y + h, x:x + w]
            try:
                result_list, _ = cls.recognize_text(roi, use_det=use_det, use_cls=use_cls, use_rec=use_rec)
            except ValueError:
                result_list = cls.recognize_text(roi, use_det=use_det, use_cls=use_cls, use_rec=use_rec)
            result_str = result_list[0][0] if result_list else None
            text_rect_list.append([result_str, rect])

        return text_rect_list

    @classmethod
    def get_best_choice(cls, text_rect_list, max_length_diff_ratio=0.6):
        max_score = -1  # 初始化最大得分为负数
        best_rect = []
        matched_str = ''

        for target, rect in text_rect_list:
            print(f'target:{target, rect}')
            target_len = len(target)
            if target_len < 2:
                continue
            filtered_choices = [choice for choice in cls._choices
                                if min(abs(len(choice) - target_len) / target_len,
                                       abs(len(choice) - target_len) / len(choice)) <= max_length_diff_ratio]

            # 现在使用限定长度差异的choices进行匹配
            result = process.extractOne(target, filtered_choices)
            if result is None:
                continue
            match = result[0]
            score = result[1]

            # 更新最佳匹配结果
            if score > max_score:
                max_score = score
                matched_str = match
                best_rect = rect

        return matched_str, best_rect, max_score


if __name__ == '__main__':
    import time

    img_path = r'C:\Users\Camreishi\PycharmProjects\Limbus-Scripts\opencv_test\output'
    start_time = time.time()
    for i in range(9):
        img_name = f'rect_100{i}.png'
        img = os.path.join(img_path, img_name)
        ocr_result = Ocr.recognize_text(
            img,
            use_det=False, use_cls=False, use_rec=True)
        print(ocr_result)
    end_time = time.time()
    print(end_time - start_time)
