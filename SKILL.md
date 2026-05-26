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

### ⚠️ PIL 环境
`/opt/hermes/.venv/bin/python` 没有 PIL，需用 uv：
```bash
uv run --with Pillow python3 your_script.py
```

### ⚠️ 生成后必须发回调用出处
**图片生成后不要只保存本地，必须通过 MEDIA: 路径发回给调用者。**

- 如果用户在群里调用 → 发回那个群
- 如果用户私信调用 → 发回那个 DM

由 Hermes Agent 根据当前会话上下文（chat_id）自动路由，无需在技能说明里指定固定 chat_id。

### ⚠️ 脚本路径注意
`mlb_image_edit_pro.py` 位于技能目录内（`/config/.hermes/skills/image-generation/mlb-image-edit-pro/scripts/`），**不在 `/config/Desktop/cwr/scripts/` 下**。使用时需要：
- 直接复制到工作目录：`cp /config/.hermes/skills/image-generation/mlb-image-edit-pro/scripts/mlb_image_edit_pro.py /config/Desktop/cwr/scripts/`
- 或直接用完整路径调用

---

## 设计资源

**AIPY 漫画风格规范**: `references/aipy-comic-style.md` — AIPY 课程/营销内容的极简线稿漫画风格定义，基于 Nano Banana Pro 的 8 格对比漫画风格。包含严格的色彩系统（灰黑线条+奶油底色+黄色强调）、线条规范、人物设计和构图原则。适用于为 AIPY 文章生成统一风格的插画和封面。

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

# 多参考图合成
cd /config/Desktop/cwr && uv run --with Pillow python3 scripts/mlb_image_edit_pro.py edit \
  -p "Place this character in this scene with this lighting" \
  -i /path/to/char.png /path/to/scene.jpg /path/to/lighting.jpg
```
