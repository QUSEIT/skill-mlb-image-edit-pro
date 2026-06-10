---
name: mlb-image-edit-pro
description: |
  MuleRun Nano Banana Pro 高保真图片编辑技能集 — 基于 Gemini Nano-Banana Pro 的图生图编辑能力。

  适用场景：高质量图片风格迁移、精细元素编辑、照片级合成、角色一致性编辑等。
  相比 Nano Banana 2 标准版，Pro 提供升级后的扩散骨干网络，在保持全局构图的同时更好地保留光照、纹理和边缘细节。

  ⚠️ 注意：此模型目前处于公测阶段，并非所有账户都有访问权限，API 请求可能不稳定。

  前置要求：环境变量 MLB_API_KEY（获取地址：https://mulerun.com 控制台）
category: image-generation
---

## 能力概览

| 能力 | 触发方式 | 说明 |
|------|----------|------|
| **高保真图片编辑** | 用户上传参考图 + 编辑指令 | Pro 级图生图编辑，保留更多细节 |
| **风格迁移** | "把这张照片变成XX风格" | 保持构图，改变整体风格，质量更高 |
| **场景重构** | "让这个人开车沿着海岸线行驶" | 基于参考图重构场景 |
| **多图合成** | 提供多张参考图 | 最多 10 张（描述写 max 14，但 schema 限制为 10） |

**模型**: Gemini Nano-Banana Pro (Beta)

**支持的宽高比** (`aspect_ratio`):
- `1:1` (默认)
- `2:3`, `3:4`, `4:5`, `9:16` — 竖版
- `3:2`, `4:3`, `5:4`, `16:9`, `21:9` — 横版

**注意**：Pro 版**不支持** `1:4`, `1:8`, `4:1`, `8:1` 这些极端比例

**分辨率** (`resolution`):
- `1K`
- `2K` (默认)

**注意**：Pro 版**不支持** `4K`，且默认是 `2K`（而非标准版的 `1K`）

---

## 与标准版 (mlb-image-edit) 的核心差异

| 维度 | Nano Banana 2 (标准版) | Nano Banana Pro |
|------|----------------------|-----------------|
| **端点** | `/nano-banana-2/edit` | `/nano-banana-pro/edit` |
| **模型** | Gemini 3.1 Flash Image Preview | Gemini Nano-Banana Pro |
| **状态** | 稳定 | **Beta 公测，可能不稳定** |
| **参考图上限** | 14 张（10 物体 + 4 角色） | **10 张** |
| **分辨率** | 1K / 2K / 4K | **1K / 2K**（无 4K） |
| **默认分辨率** | 1K | **2K** |
| **宽高比** | 14 种（含 1:4, 1:8, 4:1, 8:1） | **10 种**（不含极端比例） |
| **web_search** | ✅ 支持 | ❌ **不支持** |
| **保真度** | 标准 | **更高**（更好的光照/纹理/边缘保留） |

---

## 图片编辑 (Pro Edit)

### 执行方式

```bash
cd /config/Desktop && /opt/hermes/.venv/bin/python << 'EOF'
# 图片编辑脚本
EOF
```

或直接调用 `mlb_image_edit_pro()` 函数（见 references/api.md）。

### 典型用法

**1. 场景重构**:
> make a photo of the man driving the car down the california coastline

**2. 高保真风格迁移**:
> Transform this portrait into an oil painting style, keep facial features exact

**3. 精细元素编辑**:
> Change the background to a sunset beach, keep the person exactly the same

**4. 多图合成**:
> 提供最多 10 张参考图，Pro 会更好地保持各图的细节和一致性

### 可用参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prompt` | string | 必填 | 编辑指令 |
| `images` | list | 必填 | 参考图片列表（URL 或本地路径，1-10 张） |
| `aspect_ratio` | string | 1:1 | 输出宽高比（Pro 不支持 1:4, 1:8, 4:1, 8:1） |
| `resolution` | string | 2K | 1K / 2K（必须大写 K，无 4K） |
| `output_dir` | string | /config/Desktop | 下载目录 |
| `download` | bool | true | 是否下载到本地 |
| `poll_interval` | int | 3 | 轮询间隔（秒） |
| `max_wait` | int | 120 | 最大等待时间（秒） |

---

## 异步任务模式

与标准版相同，采用**异步任务**架构：

1. **提交任务** → POST `/nano-banana-pro/edit` → 返回 `task_info.id`
2. **轮询结果** → GET `/nano-banana-pro/edit/{task_id}` → 直到 `status: completed`

任务状态：`pending` → `processing` → `completed` / `failed`

---

## 参考图处理规则

### 支持格式
- JPEG, JPG, PNG, BMP, WEBP
- 单张最大 20MB（建议）

### 输入方式
- **URL**: 公网可访问的图片链接
- **本地文件**: 脚本自动转为 Base64 (`data:image/png;base64,{data}`)

```python
# 混合输入示例
images = [
    "https://example.com/person.png",      # URL
    "/path/to/local/background.jpg",       # 本地文件（自动转 base64）
]
```

---

## 输出处理

API 返回编辑后的图片 URL。

如需保存到本地，脚本会自动下载到 `/config/Desktop/` 目录，文件名前缀 `mlb_pro_edit_`。

---

## 常见错误

| 状态 | 含义 | 处理方式 |
|------|------|----------|
| completed | 成功 | - |
| failed | 失败 | 检查 `error` 字段详情 |
| pending/processing | 处理中 | 正常轮询等待 |

**Beta 阶段特有问题**：
- 如果返回权限错误，说明账户尚未获得 Pro 模型访问权限
- API 可能间歇性不稳定，建议增加重试逻辑

---

## 陷阱与注意事项

### ⚠️ Beta 公测限制
此模型处于公测阶段：
- 并非所有账户都有访问权限
- API 请求可能不稳定
- 功能可能随时调整

### ⚠️ 分辨率限制
- **不支持 4K**，只有 1K / 2K
- **默认是 2K**（不是标准版的 1K）

### ⚠️ 宽高比限制
Pro 版**不支持**以下极端比例：
- `1:4`, `1:8`（超长竖版）
- `4:1`, `8:1`（超长横版）

可用比例：
- `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

### ⚠️ 无 Web Search
Pro 版**不支持** `web_search` 参数，无法使用 Google Search 实时数据增强。

### ⚠️ 参考图上限 10 张
标准版支持 14 张（10 物体 + 4 角色），Pro 版最多 **10 张**。

### ⚠️ 本地文件自动转 Base64
脚本会自动将本地文件转为 `data:image/png;base64,{data}` 格式，无需手动处理。

### ⚠️ .env 路径
环境变量文件在 `/config/.hermes/.env`：
```python
from dotenv import load_dotenv
load_dotenv("/config/.hermes/.env", override=False)
```

### ⚠️ PIL + dotenv 环境
`/opt/hermes/.venv/bin/python` 没有 PIL，**也没有 python-dotenv**。必须用 uv 并指定两个包：
```bash
uv run --with Pillow,python-dotenv python3 your_script.py
```
单独 `--with Pillow` 会报 `ModuleNotFoundError: No module named 'dotenv'`。

### ⚠️ 生成后必须发回调用出处
**图片生成后不要只保存本地，必须通过 MEDIA: 路径发回给调用者。**

- 如果用户在群里调用 → 发回那个群
- 如果用户私信调用 → 发回那个 DM

由 Hermes Agent 根据当前会话上下文（chat_id）自动路由，无需在技能说明里指定固定 chat_id。

### ⚠️ OpenClaw 风格封面图 Prompt 模板（已验证）

当创作 OpenClaw 风格公众号封面图时，使用以下 Prompt 结构（基于三次成功生成经验）：

```python
prompt = """Transform this illustration into a flat vector cover illustration for an article about '[文章标题/主题]'. Create a concept illustration showing: [具体视觉元素描述——编排节点 + 并行代理网络 + 对抗性验证等核心概念]. The composition should convey [scale/control/verification 等核心信息]. Use OpenClaw warm coral-orange gradient vector style with transparent background, dynamic energy, 16:9 aspect ratio."""
```

**关键要素**：
- 明确提及 "flat vector cover illustration"
- 明确提及 "OpenClaw warm coral-orange gradient vector style with transparent background"
- 明确提及 "16:9 aspect ratio"（公众号封面标准比例）
- 视觉概念要具体：中央编排节点、并行代理流、对抗性验证对峙等
- 避免过于抽象的概念描述，模型更喜欢可视觉化的具象指令

### ⚠️ AIPY 人物设计铁律（用户强偏好）
**禁止**：光头圆球、无发线、火柴人棍状身体、纯两点一眼一嘴的极简五官。
**必须**：简洁发线 + 圆润头部 + 小鼻子 + 小弧线眉毛 + 小弧线嘴 + 干净身形。
完整规范见 `references/aipy-comic-style.md`，生成 AIPY 内容前必读该文件。

### ⚠️ OpenClaw 风格支持
当用户明确说「openclaw」/「OpenClaw」/「爪子风格」时，使用 OpenClaw 矢量渐变风格：
- **主体色**：暖珊瑚橙（`#F8704B` 主填充）+ 同色系渐变（高光 `#FFC8AA`，暗部 `#3C3230`）
- **背景/辅助色**：可使用黑白灰等中性色（`#FFFFFF`/`#F5F5F5`/`#9E9E9E`/`#1A1A1A`）
- **灵活背景**：可使用透明背景、纯白、浅灰或深灰背景
- 无描边，色块明暗交界形成轮廓
- **主体必须用暖珊瑚橙，背景可用中性色** — 不再强制所有元素同色系
- 完整规范见 `references/clawclass-style.md`
- 参考图：`/config/Desktop/cwr/images/clawclass_style.png`

### ⚠️ SilkRoad 风格支持
当用户明确说「silkroad」/「SilkRoad」/「丝路风格」时，使用 SilkRoad 扁平色块风格：
- 琥珀金主导 + 高饱和亮色点缀（蓝/红/绿）
- 透明背景（PNG alpha）
- 纯平涂色块，无渐变、无阴影、无描边
- 完整规范见 `references/silkroad-style.md`
- 参考图：`/config/Desktop/cwr/images/silkroad_style.png`

### ⚠️ 脚本路径注意
`mlb_image_edit_pro.py` 位于技能目录内（`/config/.hermes/skills/image-generation/mlb-image-edit-pro/scripts/`），**不在 `/config/Desktop/cwr/scripts/` 下**。使用时需要：
- 直接复制到工作目录：`cp /config/.hermes/skills/image-generation/mlb-image-edit-pro/scripts/mlb_image_edit_pro.py /config/Desktop/cwr/scripts/`
- 或直接用完整路径调用

---

**设计资源**

**AIPY 漫画风格规范**: `references/aipy-comic-style.md` — AIPY 课程/营销内容的极简线稿漫画风格定义，基于 Nano Banana Pro 的 8 格对比漫画风格。包含严格的色彩系统（灰黑线条+奶油底色+黄色强调）、线条规范、人物设计和构图原则。适用于为 AIPY 文章生成统一风格的插画和封面。

**OpenClaw 矢量渐变风格规范**: `references/clawclass-style.md` — 暖珊瑚橙主体色 + 中性色背景，灵活配色矢量插画风格，无描边，现代扁平感。当用户指定「openclaw」风格时启用。参考图：`/config/Desktop/cwr/images/clawclass_style.png`。

**SilkRoad 扁平色块风格规范**: `references/silkroad-style.md` — 琥珀金主导 + 高饱和亮色点缀（蓝/红/绿）的扁平矢量插画风格，透明背景，纯平涂色块，无渐变无阴影。当用户指定「silkroad」风格时启用。参考图：`/config/Desktop/cwr/images/silkroad_style.png`。

**参考脚本**: `scripts/mlb_image_edit_pro.py`（位于技能目录下，非 `/config/Desktop/cwr/scripts/`）

完整的 Pro 版图片编辑实现，包含环境加载、参考图处理、异步任务提交、轮询、图片下载和 CLI 入口。

**配套参考**:
- `references/feishu-upload.md` — 生成图片后上传到飞书文件夹的完整流程（token 获取 + curl 上传）

```bash
# 场景重构
cd /config/Desktop/cwr && uv run --with Pillow python3 scripts/mlb_image_edit_pro.py edit \
  -p "make a photo of the man driving the car down the california coastline" \
  -i /path/to/person.jpg /path/to/car.jpg

# 高保真风格迁移
cd /config/Desktop/cwr && uv run --with Pillow python3 scripts/mlb_image_edit_pro.py edit \
  -p "Transform into an oil painting style, keep facial features exact" \
  -i /path/to/portrait.png --resolution 2K
```bash
# SilkRoad 风格 — 琥珀金扁平色块
cd /config/Desktop/cwr && uv run --with Pillow python3 scripts/mlb_image_edit_pro.py edit \
  -p "Flat vector illustration with amber gold color blocks and bright accent colors" \
  -i /config/Desktop/cwr/images/silkroad_style.png --resolution 2K
```
