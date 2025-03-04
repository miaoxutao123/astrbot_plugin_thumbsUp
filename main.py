from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.all import *
import json
import os
import time
from datetime import datetime, timedelta
import asyncio

# 定义时间周期
TIME_PERIODS = {
    "daily": "%Y-%m-%d",
    "weekly": "%Y-%W",
    "monthly": "%Y-%m",
    "quarterly": "%Y-Q%q",
    "yearly": "%Y"
}

@register("水群统计", "喵喵", "统计每个群聊内每个人的发言次数", "0.1", "https://github.com/yourusername/astrbot_plugin_thumbsUp")
class GroupChatCounter(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.data_file = "group_chat_counter.json"
        self.counter = self.load_data()
        self.setup_timer()

    def load_data(self):
        """从 JSON 文件加载数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {period: {} for period in TIME_PERIODS.keys()}

    def save_data(self):
        """将数据保存到 JSON 文件"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.counter, f, ensure_ascii=False, indent=4)

    def get_current_period(self, period_type):
        """获取当前时间周期"""
        now = datetime.now()
        if period_type == "quarterly":
            quarter = (now.month - 1) // 3 + 1
            return now.strftime("%Y-Q") + str(quarter)
        return now.strftime(TIME_PERIODS[period_type])

    def setup_timer(self):
        """设置定时任务，每天检查时间周期并更新统计"""
        import asyncio

        async def check_period():
            while True:
                await asyncio.sleep(86400)  # 每天检查一次
                self.update_periods()

        asyncio.create_task(check_period())

    def update_periods(self):
        """更新时间周期统计"""
        now = datetime.now()
        for period_type in TIME_PERIODS.keys():
            current_period = self.get_current_period(period_type)
            if current_period not in self.counter[period_type]:
                self.counter[period_type][current_period] = {}
            # 清理过期周期（可选）
            self.counter[period_type] = {k: v for k, v in self.counter[period_type].items() if k == current_period}
        self.save_data()

    @filter.event_message_type(EventMessageType.GROUP_MESSAGE)  # 使用枚举类型
    async def on_group_message(self, event: AstrMessageEvent):
        """监听群聊消息并统计发言次数"""
        user_id = event.get_sender_id()
        group_id = event.message_obj.group_id

        for period_type in TIME_PERIODS.keys():
            current_period = self.get_current_period(period_type)
            if group_id not in self.counter[period_type][current_period]:
                self.counter[period_type][current_period][group_id] = {}
            if user_id not in self.counter[period_type][current_period][group_id]:
                self.counter[period_type][current_period][group_id][user_id] = 0
            self.counter[period_type][current_period][group_id][user_id] += 1
        self.save_data()

    @filter.command("水群排行榜")
    async def query_group_count(self, event: AstrMessageEvent, group_id: str):
        """查询指定群聊内所有成员的发言次数"""
        period_type = event.message_str.split()[1] if len(event.message_str.split()) > 1 else "daily"
        if period_type not in TIME_PERIODS:
            yield event.plain_result("不支持的时间周期，请使用 daily、weekly、monthly、quarterly 或 yearly。")
            return

        current_period = self.get_current_period(period_type)
        if group_id not in self.counter[period_type][current_period]:
            yield event.plain_result(f"群组 {group_id} 在当前 {period_type} 周期内还没有发言记录。")
            return

        result = f"群组 {group_id} 在当前 {period_type} 周期内的发言次数统计：\n"
        for user_id, count in self.counter[period_type][current_period][group_id].items():
            user_name = event.get_member_name(user_id)  # 获取用户昵称
            result += f"{user_name}({user_id}): {count}次\n"
        yield event.plain_result(result)

# @register("点赞", "喵喵", "点赞", "1.0", "https://github.com/miaoxutao123/astrbot_plugin_thumbsUp")
# class MyPlugin(Star):
#     def __init__(self, context: Context,config: dict):
#         super().__init__(context)
#         self.tunum = config.get("thnum")
#         self.response_str = config.get("response_str")

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