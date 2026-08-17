from astrbot.api import AstrBotPlugin
from astrbot.api.event import AstrMessageEvent
from astrbot.api.llm import LLMRequest

plugin = AstrBotPlugin(
    "astrbot_plugin_channel_meta_inject",
    "渠道元数据注入",
    "1.0.0",
    "custom"
)

@plugin.on_llm_request
async def inject_meta(event: AstrMessageEvent, llm_req: LLMRequest):
    plat = event.get_platform_name()
    umo = event.unified_msg_origin
    sender_id = event.get_sender_id()
    is_group = event.is_group()

    # 注入到请求顶层extra_params（透传给agentx/openai兼容接口）
    llm_req.extra_params["ast_platform"] = plat
    llm_req.extra_params["ast_sender_id"] = sender_id
    llm_req.extra_params["ast_unified_msg_origin"] = umo
    llm_req.extra_params["ast_is_group"] = is_group

plugin.register()
