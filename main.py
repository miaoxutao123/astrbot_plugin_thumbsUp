from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.all import *
import json

@register("点赞", "喵喵", "点赞测试", "0.1", "https://github.com/miaoxutao123/astrbot_plugin_thumbsUp")
class MyPlugin(Star):
    def __init__(self, context: Context,config: dict):
        super().__init__(context)
        self.tunum = config.get("thnum")
        self.response_str = config.get("response_str")
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("点赞")
    async def helloworld(self, event: AstrMessageEvent):
        num = self.tunum
        response_str = self.response_str
        if event.get_platform_name() == "aiocqhttp":
            # qq
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot # 得到 client
            message_id = event.get_message_id()
            payloads = {
                "message_id": message_id,  # 添加 message_id
                "user_id": event.get_sender_id(),
                "times": num
            }
            ret = await client.api.call_action('delete_msg', **payloads) # 调用 协议端  API
            logger.info(f"delete_msg: {ret}")
            yield event.plain_result(f"{response_str}")