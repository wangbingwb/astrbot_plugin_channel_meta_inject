# astrbot_plugin_channel_meta_inject

> AstrBot 渠道元数据注入插件

在每次 LLM 上行请求体顶层自动注入渠道标识信息，用于区分消息来源（微信、QQ、Telegram 等），便于 downstream 服务进行统计分析与路由。

## 功能

利用 `on_llm_request` 钩子，在 AstrBot 调用 LLM 前，将以下渠道元数据写入 `ProviderRequest.extra_params`：

| 字段 | 说明 | 示例值 |
|---|---|---|
| `ast_platform` | 平台适配器名称 | `aiocqhttp`、`telegram`、`discord` |
| `ast_sender_id` | 发送者 ID | 用户 QQ 号、Telegram user id 等 |
| `ast_unified_msg_origin` | 统一消息来源标识 | 群 ID / 私聊标识 |
| `ast_is_group` | 是否为群聊 | `True` / `False` |

这些字段会随请求透传给 AgentX / OpenAI 兼容接口，可在后端直接读取用于：

- 按渠道统计 LLM 调用量
- 区分私聊 / 群聊场景
- 基于来源做请求路由或审计

## 支持平台

aiocqhttp · qq_official · telegram · discord · slack · kook · satori · misskey · line · lark · dingtalk · wecom · weixin_official_account

## 要求

- AstrBot `>= 4.16, < 5`

## 安装

1. 将本仓库克隆到 AstrBot 插件目录：

   ```bash
   cd <AstrBot>/data/plugins
   git clone https://github.com/wangbingwb/astrbot_plugin_channel_meta_inject.git
   ```

2. 在 AstrBot WebUI 插件页面确认插件已加载，或重启 AstrBot。

## 工作原理

```
用户消息 → 平台适配器 → AstrBot Core
                            ↓
                   on_llm_request 钩子触发
                            ↓
               本插件注入 ast_* 字段到 extra_params
                            ↓
                 LLM Provider（OpenAI 兼容接口）
```

## License

MIT
