import configparser
import os

from workbench.file_path_utils import PathManager


class SettingsReader:
    config_path = os.path.join(PathManager.ROOT_RELPATH, 'settings.ini')
    config = configparser.ConfigParser()
    encoding = 'utf-8'

    @classmethod
    def read_option(cls, section, option):
        cls.config.read(cls.config_path, encoding=cls.encoding)
        return cls.config.get(section, option)

    @classmethod
    def read_option_language(cls, section, option):
        lang = cls.read_option(section, option)
        lang_data = {
            'en': "English",
            'jp': "日本語",
            'kr': "한국어",
            'zh':"零协汉化",
        }
        return lang_data[lang]

    @classmethod
    def set_option(cls, section, option, value):
        cls.config.read(cls.config_path, encoding=cls.encoding)
        cls.config.set(section, option, value)
        cls.write_config()

    @classmethod
    def write_config(cls):
        with open(cls.config_path, 'w', encoding=cls.encoding) as config_file:
            cls.config.write(config_file)


# 示例用法
if __name__ == '__main__':
    # 读取当前设置
    language_current = SettingsReader.read_option('Language', 'current')
    print(f"当前语言: {language_current}")

    shortcut1 = SettingsReader.read_option('Shortcut', 'shortcut1')
    shortcut2 = SettingsReader.read_option('Shortcut', 'shortcut2')
    print(f"快捷键1: {shortcut1}, 快捷键2: {shortcut2}")

    # 设置新的语言并保存到文件
    SettingsReader.set_option('Language', 'current', 'jp')
    new_language = SettingsReader.read_option('Language', 'current')
    print(f"已将当前语言设置为: {new_language}")

    # 更改快捷键设置
    SettingsReader.set_option('Shortcut', 'shortcut1', 'P')
    new_shortcut1 = SettingsReader.read_option('Shortcut', 'shortcut1')
    print(f"已将快捷键1设置为: {new_shortcut1}")
