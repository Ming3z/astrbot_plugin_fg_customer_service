import re

from astrbot.api import logger
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register


def replace_urls_in_string(input_str: str, replacement: str = 'url') -> str:
    """
    检测字符串中所有类型的 URL 并将其替换为指定的字符串。

    这个函数使用一个强大的正则表达式来匹配各种形式的 URL，
    包括 http, https, ftp, 以及以 www. 开头的链接。

    Args:
        input_str (str): 需要处理的原始字符串。
        replacement (str): 用于替换 URL 的字符串，默认为 'url'。

    Returns:
        str: 将所有 URL 替换后的新字符串。
    """
    # 这个正则表达式可以匹配大多数常见的 URL 格式
    # 解释:
    # (https?://[^\s'"]+|www\.[^\s'"]+)
    # 1. https?://[^\s'"]+ : 匹配以 http:// 或 https:// 开头的 URL。
    #    - https?:// : 匹配 'http://' 或 'https://' ('s' 是可选的)
    #    - [^\s'"]+ : 匹配一个或多个非空白、非单引号、非双引号的字符。这确保了 URL 在遇到空格或引号时会停止匹配。
    # 2. | : 或操作符
    # 3. www\.[^\s'"]+ : 匹配以 'www.' 开头的 URL。
    url_pattern = r"(https?://[^\s'\"<>()]+|www\.[^\s'\"<>()]+)"

    # 使用 re.sub() 进行查找和替换
    # 它会找到所有匹配 pattern 的子串，并用 replacement 替换它们
    return re.sub(url_pattern, replacement, input_str)


@register("test", "ymk", "测试插件", "0.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        logger.info("实例化插件")

    async def terminate(self):
        logger.info("插件被卸载/停用")

    # 注册所有消息监听
    @filter.event_message_type(filter.EventMessageType.ALL)
    async def on_all_message(self, event: AstrMessageEvent):

        # 打印完整数据
        message_str = str(event.message_obj)
        logger.debug(f"full data = {message_str}")

        # 回复消息
        attachment = hasattr(event.message_obj.raw_message, "attachments") and event.message_obj.raw_message.attachments
        if attachment and attachment[0]:
            yield event.plain_result(f"收到附件类型：{attachment[0].content_type}")
        else:
            yield event.plain_result(f"收到消息：{replace_urls_in_string(event.message_str)}")
        yield event.plain_result(f"完整数据（若有 URL 将被替换至域名部分）：{replace_urls_in_string(message_str)}")
