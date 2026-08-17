from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest
from astrbot.core.agent.message import TextPart


@register(
    "astrbot_plugin_channel_meta_inject",
    "wangbing",
    "渠道元数据注入",
    "1.0.0",
)
class ChannelMetaInjectPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.on_llm_request()
    async def inject_meta(
        self, event: AstrMessageEvent, req: ProviderRequest
    ):
        plat = event.get_platform_name()
        sender_id = event.get_sender_id()
        is_group = event.is_group()

        # 将渠道元数据注入为临时用户内容附加部分（不污染对话历史）
        meta_text = (
            f"<channel_meta>\n"
            f"platform: {plat}\n"
            f"sender_id: {sender_id}\n"
            f"is_group: {is_group}\n"
            f"unified_msg_origin: {event.unified_msg_origin}\n"
            f"</channel_meta>"
        )
        part = TextPart(text=meta_text)
        part.mark_as_temp()  # 标记为临时，不持久化到历史记录
        req.extra_user_content_parts.append(part)
