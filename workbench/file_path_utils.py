import os


class PathManager:
    """
    PathManager class manages the essential file paths and language list for the application.

    Attributes:
        CURRENT_PATH (str): The absolute path to the current script file.
        CURRENT_DIR (str): The directory containing the current script file.
        ROOT_RELPATH (str): The relative path to the root.
        ASSETS_RELPATH (str): The relative path to the assets.
        LANGUAGE_LIST (List[str]): A list of supported languages, including "English", "Japanese", and "Korean".

    Methods:
        get_local_image(image_name: str) -> str or None:
            Looks up and returns the local path of the specified image file. It checks the root directory first,
            then iterates through the language directories in the `LANGUAGE_LIST`.
    """

    CURRENT_PATH = os.path.abspath(__file__)
    CURRENT_DIR = os.path.dirname(CURRENT_PATH)
    ROOT_RELPATH = os.path.join(CURRENT_DIR, '../')
    ASSETS_RELPATH = os.path.join(CURRENT_DIR, '../assets')
    LANGUAGE_LIST = ["English", "Japanese", "Korean"]

    @classmethod
    def get_local_image(cls, image_name: str) -> str or None:
        """Find and return the local path of the specified image file. Check the root directory first,
        then traverse through the language directories in the `LANGUAGE_LIST`.

        Args:
            image_name (str): The name of the image file to be located.

        Returns:
            str or None: The local path of the found image file, or None if not found.
        """
        path = os.path.join(cls.ASSETS_RELPATH, image_name)

        if os.path.isfile(path):
            return path

        for lang in cls.LANGUAGE_LIST:
            lang_path = os.path.join(cls.ASSETS_RELPATH, lang, image_name)
            if os.path.isfile(lang_path):
                return lang_path

        return None


if __name__ == '__main__':
    result = PathManager.get_local_image('back_button.png')
    print(result)
