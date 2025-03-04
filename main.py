from astrbot.api.all import *

from datetime import datetime, timedelta
import asyncio


@register("点赞", "喵喵", "点赞", "1.0", "https://github.com/miaoxutao123/astrbot_plugin_thumbsUp")
class MyPlugin(Star):
    def __init__(self, context: Context,config: dict):
        super().__init__(context)
        self.tunum = config.get("thnum")
        self.response_str = config.get("response_str")

    @filter.command("赞我")
    async def helloworld(self, event: AstrMessageEvent):
        num = self.tunum
        response_str = self.response_str
        if event.get_platform_name() == "aiocqhttp":
            # qq
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot # 得到 client
            payloads = {
                "user_id": event.get_sender_id(),
                "times": num
            }
            ret = await client.api.call_action('send_like', **payloads) # 调用 协议端  API
            logger.info(f"send_like: {ret}")
            yield event.plain_result(f"{response_str}")