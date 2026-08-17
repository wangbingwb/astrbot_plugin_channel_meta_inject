from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest


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
        umo = event.unified_msg_origin
        sender_id = event.get_sender_id()
        is_group = event.is_group()

        # 注入到请求顶层 extra_params（透传给 agentx/openai 兼容接口）
        req.extra_params["ast_platform"] = plat
        req.extra_params["ast_sender_id"] = sender_id
        req.extra_params["ast_unified_msg_origin"] = umo
        req.extra_params["ast_is_group"] = is_group
