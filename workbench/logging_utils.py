import logging
import os

from colorlog import ColoredFormatter

from workbench.file_path_utils import PathManager


class LoggingManager:
    # noinspection SpellCheckingInspection
    log_file_path = os.path.join(PathManager.LOG_RELPATH, 'Limbug_Clicker.log')
    logger = logging.getLogger('my_logger')
    logger.propagate = False
    # 清除logger上的处理器
    if len(logger.handlers) > 0:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    logger.setLevel(logging.DEBUG)
    # 创建FileHandler和StreamHandler
    fh = logging.FileHandler(log_file_path, mode='w')
    # fh.setLevel(logging.CRITICAL)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = ColoredFormatter('%(asctime)s - %(levelname)s: %(filename)s[line:%(lineno)d] - %(message)s')
    ch_formatter = ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s: %(filename)s[line:%(lineno)d] - %(message)s')
    ch.setFormatter(ch_formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    @classmethod
    def toggle_logging(cls, is_enabled: bool):
        if is_enabled:
            cls.fh.setLevel(logging.DEBUG)
        else:
            cls.fh.setLevel(logging.CRITICAL)

# 使用示例：
# from workbench.logging_utils import LoggingManager
#
# if __name__ == '__main__':
#
#     # 改变日志级别
#     logger = LoggingManager.logger
#     LoggingManager.toggle_logging(True)  # 将日志级别切换到DEBUG（假设我们希望看到详细的调试信息）
#
#     # 使用logger记录一条info消息
#     logger.info('Hello from the test.')
#
#     # 模拟一个异常并记录错误信息
#     # noinspection PyBroadException
#     try:
#         res = 0 / 0
#     except Exception as exc:
#         logger.exception("An error occurred: ")
#
#     # 如果需要，还可以再次改变日志级别
#     LoggingManager.toggle_logging(False)  # 将日志级别切换回CRITICAL或更高
