# SilkRoad 扁平色块风格规范

> 基于飞书文件 `WfVFbQDuQouPqTxluFGc1vGLnvc` 提取的扁平矢量插画风格
> 适用场景：AIPY 课程/营销内容的现代扁平图标、概念图、插画
> 触发关键词：用户说「silkroad」/「SilkRoad」/「丝路风格」

---

## 色彩系统（严格）

| 角色 | 色值 | 用途 |
|------|------|------|
| **主色（浅）** | `#FFD29B` ~ `#FED8A0` | 暖桃金，大面积填充、背景色块 |
| **主色（中）** | `#FFB932` ~ `#F8B830` | 琥珀金，主体元素填充 |
| **主色（深）** | `#FFA500` ~ `#F0A000` | 深琥珀橙，暗部、强调 |
| **点缀蓝** | `#0078F0` ~ `#0070E8` | 明亮蓝，小面积点缀（5-15%） |
| **点缀红** | `#FF4146` ~ `#F04045` | 珊瑚红，小面积点缀（5-15%） |
| **点缀绿** | `#0ACD64` ~ `#08C860` | 明亮绿，小面积点缀（5-15%） |
| **背景** | **透明** (alpha=0) | 无背景色，PNG 透明底 |

**色彩铁律：**
- 金色/琥珀色家族为绝对主导（占画面 70%+）
- 蓝、红、绿仅作为小面积点缀色使用（各占 5-15%）
- 所有颜色均为**高饱和、高亮度**，明快活泼
- 无渐变、无阴影过渡，纯平涂色块
- 无纯黑 `#000000` 描边或填充
- 整体画面温暖、明快、现代、友好

---

## 色块与轮廓规范

- **纯平涂**：每个形状使用单一纯色填充，无渐变、无纹理
- 轮廓由**色块边界**自然形成，无额外描边
- 边缘干净、矢量感强
- 圆角处理柔和，几何形状简洁

---

## 人物设计

- **头部**：简洁发型轮廓，面部极简（两点眼 + 弧线嘴），无鼻子
- **身体**：极简几何化，肢体动态通过姿态表达
- **比例**：头身比可适度夸张，偏现代卡通
- **着色**：使用金色家族平涂，点缀色用于服饰/道具细节

**人物风格铁律：**
- ❌ 禁止光头、禁止简单几何圆圈头
- ✅ 必须有发型轮廓
- ✅ 面部保持极简

**当无人物时**，画面可以仅有：
- 工具/设备的扁平矢量图标（手机、电脑、代码符号）
- 几何形状的组合与连接
- 抽象图形与纯色块拼接

---

## 背景

- **完全透明**（PNG with alpha），无背景色块
- 元素独立悬浮，适配任意背景
- 无多余装饰性背景元素

---

## Prompt 模板（用于 MLB Pro 编辑）

```
Flat vector illustration, bold solid color blocks, transparent background.
Modern icon-style design with clean geometric shapes.

[人物场景：Character with simple hairstyle, minimal facial features, geometric body in dynamic pose. OR 非人物场景：Flat vector icons and geometric shapes only]

Color palette (STRICT):
- Primary light: warm peach gold (#FFD29B)
- Primary medium: amber gold (#FFB932)
- Primary dark: deep amber (#FFA500)
- Accent blue: bright blue (#0078F0) - small areas only
- Accent red: coral red (#FF4146) - small areas only
- Accent green: bright green (#0ACD64) - small areas only
- NO gradients, NO shadows, NO textures
- NO black outlines or fills
- NO background color, transparent PNG
- Solid flat color fills only

Clean vector edges, rounded corners, simple geometric forms.
```

---

## 参考文件

- 参考图 PNG：`/config/Desktop/cwr/images/silkroad_style.png`
- 飞书源文件：`https://iwwtpmp09eo.feishu.cn/file/WfVFbQDuQouPqTxluFGc1vGLnvc`
- 生成技能：`mlb-image-edit-pro` (Nano Banana Pro)
- 默认参数：`--resolution 2K --ratio [按需]`

---

## 风格对比

| 维度 | 极简线稿风格（默认） | OpenClaw 矢量渐变 | SilkRoad 扁平色块 |
|------|---------------------|-------------------|------------------|
| 背景 | 奶油色 `#F5F0E8` | 透明 | 透明 |
| 轮廓 | 灰黑细线 `#4A4A4A` | 无描边，明暗交界 | 无描边，色块边界 |
| 着色 | 无填充/极简点缀 | 同色系渐变填充 | 纯平涂高饱和色块 |
| 质感 | 建筑草图/蓝图感 | 现代扁平矢量感 | 现代图标/插画感 |
| 色彩范围 | 暖灰调，低饱和 | 珊瑚橙单色系 | 琥珀金主导+亮色点缀 |
| 渐变 | 无 | 柔和同色系渐变 | 无，纯平涂 |
| 人物身体 | 火柴人/细线条 | 极简几何化色块 | 极简几何化色块 |
