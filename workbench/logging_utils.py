import logging
import os

from colorlog import ColoredFormatter

import file_path_utils  # 假设这是提供获取日志文件路径的模块


class LoggingManager:
    def __init__(self, log_name='my_logger'):
        self.log_file_path = os.path.join(file_path_utils.log_relpath, 'Limbug_Clicker.log')

        self.logger = logging.getLogger(log_name)
        self.logger.propagate = False

        # 清除logger上的处理器
        if len(self.logger.handlers) > 0:
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)

        self.initialize_logger()

    def initialize_logger(self):
        self.logger.setLevel(logging.DEBUG)

        # 创建FileHandler和StreamHandler
        fh = logging.FileHandler(self.log_file_path, mode='w')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = ColoredFormatter('%(asctime)s - %(levelname)s: %(filename)s[line:%(lineno)d] - %(message)s')
        ch_formatter = ColoredFormatter(
            '%(log_color)s%(asctime)s - %(levelname)s: %(filename)s[line:%(lineno)d] - %(message)s')
        ch.setFormatter(ch_formatter)
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def toggle_logging(self, is_enabled: bool):
        if is_enabled:
            print(logging.getLevelName(self.logger.level))
            self.logger.setLevel(logging.DEBUG)
        else:
            print(logging.getLevelName(self.logger.level))
            self.logger.setLevel(logging.CRITICAL)

    def get_logger(self):
        return self.logger


# 创建并初始化全局的日志管理器实例
logging_manager = LoggingManager()


# 提供一个公共接口来访问这个日志器
def get_logger_instance():
    return logging_manager.get_logger()


# 可选地，直接导出日志管理器作为模块级别的变量（如果需要）
__all__ = ['logging_manager', 'get_logger_instance']

# 使用示例：
# from logging_utils import logging_manager, get_logger_instance
# logger = get_logger_instance()
# logging_manager.toggle_logging(True)
if __name__ == '__main__':
    # 创建一个LoggingManager实例
    log_manager = LoggingManager()

    # 获取logger实例
    logger = log_manager.get_logger()

    # 打印初始日志级别
    print(logging.getLevelName(logger.level))

    # 改变日志级别
    log_manager.toggle_logging(True)  # 将日志级别切换到DEBUG（假设我们希望看到详细的调试信息）
    print(logging.getLevelName(logger.level))

    # 使用logger记录一条info消息
    logger.info('Hello from the test.')

    # 模拟一个异常并记录错误信息
    try:
        res = 0 / 0
    except Exception as exc:
        logger.exception("An error occurred: ")

    # 如果需要，还可以再次改变日志级别
    log_manager.toggle_logging(False)  # 将日志级别切换回CRITICAL或更高
