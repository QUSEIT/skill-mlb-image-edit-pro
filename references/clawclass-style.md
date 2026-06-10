# OpenClaw 矢量渐变风格规范

> 基于飞书文件 `NOugbTjEZoNV4QxlYPGcaIr9nRg` 提取的矢量插画风格
> 适用场景：AIPY 课程/营销内容的现代扁平矢量插画、图标、概念图
> 触发关键词：用户说「openclaw」/「OpenClaw」/「爪子风格」

---

## 色彩系统（灵活）

> **核心原则**：暖珊瑚橙主色用于核心主体（人物/核心元素），背景和辅助元素可使用黑白灰等中性色。不再强制全部元素使用同一色相。

### 主体色（核心元素）

|| 角色 | 色值 | 用途 |
||------|------|------|
|| **主填充色** | `#F8704B` ~ `#FA7050` | 人物/核心主体色块填充，暖珊瑚橙 |
|| **高光/亮部** | `#FFC8AA` ~ `#FED8C0` | 受光面、高光区域，柔和蜜桃 |
|| **中间调** | `#A0503C` ~ `#C85040` | 过渡明暗，锈红/砖红 |
|| **暗部/阴影** | `#644137` ~ `#3C3230` | 阴影、轮廓暗面，深暖灰棕 |

### 背景/辅助色（可灵活使用）

|| 角色 | 色值 | 用途 |
||------|------|------|
|| **背景** | `#FFFFFF` / `#F5F5F5` / `#1A1A1A` | 纯白/浅灰/深灰背景，透明或纯色 |
|| **中性灰** | `#9E9E9E` / `#757575` | 背景装饰元素、辅助形状 |
|| **黑白对比** | `#000000` / `#FFFFFF` | 高对比轮廓、分隔线 |

**色彩铁律：**
- ✅ 核心主体（人物、核心视觉焦点）：必须使用暖珊瑚橙色系
- ✅ 背景和辅助元素：可以使用黑白灰，不强制同色系
- ✅ 通过**明度变化**和**饱和度变化**塑造主体体积感
- ❌ 背景避免使用高饱和彩色（保留给主体）
- ❌ 无纯黑 `#000000` 用于主体描边，暗部用深暖灰棕自然过渡
- ❌ 背景不使用蓝紫绿等冷色干扰主体

---

## 渐变与明暗规范

- 使用**柔和渐变**在同一色相内从亮到暗过渡
- 亮部偏蜜桃粉橙，暗部偏深棕红
- 渐变边缘自然，无硬切
- 透明背景上的元素需有完整的明暗层次

---

## 线条与轮廓规范

- 无传统意义上的"线条描边"
- 轮廓由**色块明暗交界**自然形成
- 边缘干净、矢量感强
- 圆角处理柔和，无尖锐棱角

---

## 人物设计

- **头部**：简洁发型轮廓，面部极简（两点眼 + 弧线嘴），无鼻子
- **身体**：极简几何化，肢体动态通过姿态表达
- **比例**：头身比可适度夸张，偏现代卡通
- **着色**：使用同色系渐变表现体积，无描边

**人物风格铁律：**
- ❌ 禁止光头、禁止简单几何圆圈头
- ✅ 必须有发型轮廓
- ✅ 面部保持极简

**当无人物时**，画面可以仅有：
- 工具/设备的扁平矢量轮廓（手机、电脑、代码符号）
- 几何形状的组合与连接
- 抽象图形与渐变填充

---

## 背景

- **灵活背景**：可使用透明背景（PNG alpha）、纯白、浅灰或深灰背景
- 背景装饰元素可使用黑白灰中性色
- 主体元素独立悬浮，视觉焦点清晰
- 无多余装饰性背景元素

---

## Prompt 模板（用于 MLB Pro 编辑）

```
Flat vector illustration, warm coral-orange gradient style for main subjects, flexible background colors.
Modern minimal design with soft gradient shading.

[人物场景：Character with simple hairstyle, minimal facial features, geometric body in dynamic pose. OR 非人物场景：Flat vector icons and geometric shapes only]

Color palette (FLEXIBLE):
- Main subject: warm coral (#F8704B) with peach highlights (#FFC8AA), rust mid-tones (#A0503C), dark shadows (#3C3230)
- Background/auxiliary elements: CAN use white (#FFFFFF), gray (#9E9E9E), or black (#1A1A1A) — NOT forced to match subject hue
- NO pure black outlines on main subjects, use dark warm gray-brown for shadows
- NO blue/green/purple accents on background that compete with main subject
- Gradient transitions within orange-coral family for MAIN SUBJECTS ONLY

Clean vector edges, rounded corners, no sharp angles.
```

---

## 参考文件

- 参考图 PNG：`/config/Desktop/cwr/images/clawclass_style.png`
- 飞书源文件：`https://iwwtpmp09eo.feishu.cn/file/NOugbTjEZoNV4QxlYPGcaIr9nRg`
- 生成技能：`mlb-image-edit-pro` (Nano Banana Pro)
- 默认参数：`--resolution 2K --ratio [按需]`

---

## 与 AIPY 极简线稿风格的区别

| 维度 | 极简线稿风格（默认） | OpenClaw 矢量渐变风格 |
|------|---------------------|----------------------|
| 背景 | 奶油色 `#F5F0E8` | 透明/白/灰/深灰（灵活） |
| 轮廓 | 灰黑细线 `#4A4A4A` | 无描边，明暗交界形成轮廓 |
| 着色 | 无填充/极简点缀 | 同色系渐变填充 |
| 质感 | 建筑草图/蓝图感 | 现代扁平矢量感 |
| 色彩范围 | 暖灰调，低饱和 | 珊瑚橙主色+中性背景，中高饱和 |
