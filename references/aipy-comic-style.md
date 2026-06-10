# AIPY 漫画风格规范

> 基于 Nano Banana Pro 生成的 8 格对比漫画风格定义
> 适用场景：AIPY 课程/营销内容的插画、对比图、概念图

---

## 色彩系统

| 角色 | 色值 | 用途 |
|------|------|------|
| **灰黑** | `#4A4A4A`（偏灰，非纯黑） | 所有轮廓线、人物、文字、边框 |
| **浅奶油** | `#F5F0E8` | 背景底色 |
| **黄色** | `#F5C842` | 唯一亮色，仅用于光源/重点强调 |
| **淡蓝灰** | `#B8C4CE` | 极克制，仅屏幕微光，几乎不可见 |

**色彩铁律：**
- 黄色是唯一高饱和度颜色，每格最多出现 3-4 处
- 淡蓝灰必须 muted 到接近灰色，不抢眼
- 无绿色、无粉色、无其他彩色

---

## 线条规范

- **粗细**：Ultra-thin，0.5-1px 级别
- **颜色**：偏灰的黑色（`#4A4A4A`），避免纯黑 `#000000` 的生硬感
- **风格**：建筑蓝图/工程草图质感，干净、精确、不抖动

---

## 人物设计

- **头部**：简单圆圈，无复杂发型
- **身体**：细线条身体，极简
- **五官**：两点作眼，小弧线作嘴，无鼻子
- **动态**：通过肢体角度表达情绪，不依赖面部表情

---

## 背景规范

- **底色**：浅奶油色（`#F5F0E8`），非纯白
- **纹理**：faint 点阵网格或细线纹理，均匀分布，不抢内容
- **装饰**：无多余装饰元素，背景不堆砌

---

## 构图原则

- **留白**：每格画面 spacious，元素之间留足呼吸空间
- **内容**：每格只表达一个核心动作/状态
- **对比**：上下排通过同一元素的「状态变化」形成叙事对比（如：灯亮→灯灭→灯亮）

---

## 典型对比元素（8格漫画模板）

| 元素 | 上排（旧方式） | 下排（新方式） |
|------|---------------|---------------|
| 台灯 | 亮 → 暗/闪烁 → 灭 | 亮 → 更亮 → 最亮 |
| 屏幕 | 报错/天书 | 简洁界面/AI协作 |
| 人物状态 | 兴奋 → 挫败 → 放弃 | 希望 → 轻松 → 成功 |
| 环境 | 逐渐灰暗 | 逐渐明亮 |

---

## Prompt 模板（用于 MLB Pro 编辑）

```
A wide-format cover illustration for a tech education article.
Style: Ultra-thin gray-black pen lines (#4A4A4A) on cream background (#F5F0E8) with subtle faint dot-grid texture. EXTREMELY minimal, like architectural blueprint sketches.
Characters: simple circle heads, minimal thin-line bodies, tiny dot eyes, small arc mouths.

Color palette (STRICT):
- Gray-black lines (#4A4A4A) for all outlines, characters, borders
- Cream background (#F5F0E8) with faint uniform dot-grid texture
- YELLOW (#F5C842) ONLY for light sources and key emphasis (max 3-4 spots)
- Blue-gray (#B8C4CE) ONLY for screen glow, extremely muted
NO green, NO pink, NO other colors.

[Scene-specific description...]

NO text embedded in the image. NO speech bubbles. NO complex backgrounds. Spacious, minimal, clean.
```

---

## 文件关联

- 本地规范文件：`/config/Desktop/cwr/images/aipy-style.md`
- 参考图风格来源：`https://iwwtpmp09eo.feishu.cn/file/RpsxbYaYyomDBMx0JYhcV55JnPe`
- 生成技能：`mlb-image-edit-pro` (Nano Banana Pro)
- 默认参数：`--resolution 2K --ratio 21:9`
