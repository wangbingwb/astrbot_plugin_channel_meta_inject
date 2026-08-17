# astrbot_plugin_channel_meta_inject

> AstrBot 渠道元数据注入插件

在每次 LLM 请求时，自动将渠道标识信息（平台、发送者、群聊等）注入到用户消息中，便于下游服务（AgentX / OpenAI 兼容接口）进行统计分析与路由。

## 功能

利用 `on_llm_request` 钩子，在 AstrBot 调用 LLM 前，将以下渠道元数据以 `<channel_meta>` 标签的形式注入到用户消息内容中：

| 字段 | 说明 | 示例值 |
|---|---|---|
| `platform` | 平台适配器名称 | `aiocqhttp`、`telegram`、`discord` |
| `sender_id` | 发送者 ID | 用户 QQ 号、Telegram user id 等 |
| `is_group` | 是否为群聊 | `True` / `False` |
| `unified_msg_origin` | 统一消息来源标识 | 群 ID / 私聊标识 |

注入后，下游服务收到的 user message 中会包含如下内容：

```xml
<channel_meta>
platform: aiocqhttp
sender_id: 123456
is_group: True
unified_msg_origin: group:123456
</channel_meta>
```

可在后端解析该标签用于：

- 按渠道统计 LLM 调用量
- 区分私聊 / 群聊场景
- 基于来源做请求路由或审计

> **注意**：注入的内容通过 `mark_as_temp()` 标记为临时消息，**不会持久化到对话历史**中。

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
          本插件注入 <channel_meta> 到 extra_user_content_parts
          （标记为临时，不写入对话历史）
                            ↓
                 LLM Provider（OpenAI 兼容接口）
                            ↓
              下游服务从 user message 中解析渠道元数据
```

## License

MIT
