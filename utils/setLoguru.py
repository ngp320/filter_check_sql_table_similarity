import sys

from loguru import logger


def setLoguru():
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> " \
          "<level><red>|</red>" \
          "{level}<red>|</red>" \
          "{file}<red>:</red> " \
          "{function} <red>:</red>" \
          "L{line} " \
          "{message}</level> "

    #  多线程 就 显示线程吧, 现在已经有点拥挤了
    # fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> " \
    #       "<level><red>|</red> " \
    #       "{level} <red>|</red> " \
    #       "{thread.name}<red>:</red>" \
    #       "{thread.id} <red>|</red> " \
    #       "{file}<red>:</red> " \
    #       "{function} <red>:</red>" \
    #       "L{line} - " \
    #       "{message}</level> "
    # logger.add 不能分多行
    logger.remove(handler_id=None)  # 清除之前的设置
    logger.add(sys.stderr, format=fmt, level="INFO", colorize=True)
    # 设置生成日志文件，每天10MB切割，保留3天，utf-8编码，异步写入，zip压缩
    logger.add("logs/runtime.log", level="DEBUG", rotation='10MB',
               retention='3 days',
               encoding="utf-8", enqueue=True, compression="zip")
    # log日志 分几层, 后期容易处理
    logger.add("logs/runError.log", level="ERROR", encoding="utf-8")
    logger.add("logs/runWarning.log", level="WARNING", encoding="utf-8")
    logger.add("logs/runInfo.log", level="INFO", encoding="utf-8")
