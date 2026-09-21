---
name: livephoto-wallpaper
description: 苹果原生实况壁纸（Live Photo Wallpaper）制作引擎。将用户上传的视频合成为 100% 绕过 iOS 17+ 锁屏壁纸校验的原生 Live Photo（配对 .JPG 与 .MOV）。
---

# LivePhoto-Wallpaper AI 交互与执行规范

本技能规范供各类 AI 客户端（如 WorkBuddy、Cursor、Claude Code、Open-Interpreter 等）在调用 `livephoto-wallpaper` 仓库时执行。

---

## 阶段一：首触引导漏斗（优先推送快捷指令实体文件）

当用户在移动端首次发送本仓库链接或触发本技能时，AI Agent 应直接从仓库读取 `shortcuts/实况壁纸入库.shortcut`，作为聊天文件附件直接发送至聊天框，并输出引导文案：

```text
🎉 苹果原生实况壁纸制作助手已就绪！

为了制作完成后能将实况壁纸【一键无痕存入 iPhone 相册】，我已经为您准备好配套的官方快捷指令文件：
👉 请先点击我刚发送给您的【实况壁纸入库.shortcut】文件进行添加（iPhone 会自动唤起快捷指令，只需添加一次）。

添加完成后，请直接把您想做成锁屏壁纸的【视频文件】发送给我！
```

---

## 阶段二：输入校验与拦截规则（核心约束）

### 1. 格式强校验
- **允许的输入格式**：仅限视频文件（`.mov`, `.mp4`, `.m4v`）。
- **拦截的输入格式**：任何静态图片（`.jpg`, `.jpeg`, `.png`, `.heic`, `.webp` 等）。

### 2. 图片拦截与引导话术
若检测到用户上传了图片（例如从 iPhone 相册直接选中实况照片发送到聊天框，由于系统限制通常仅发送了静态 `.jpg`），**必须立即拦截并友好提示**：

```text
⚠️ 检测到您上传的是图片文件（.jpg）。

由于手机系统机制，直接在聊天窗口发送实况图时，默认只会发送静态 JPG 封面，丢失了底层视频数据。

如需将这张 Live 图制作为完美锁屏实况壁纸，请按以下步骤操作：
  1. 在 iPhone「照片」中打开该实况图
  2. 点击右上角「···」菜单
  3. 选择【存储为视频】
  4. 将导出的视频发送给我

我将立即为您重新合成为完美支持 iOS 锁屏动态效果的 Live Photo！
```

---

## 阶段三：引擎执行与数据注入（纯跨平台通用：Linux / macOS / Docker）

底层引擎采用全通用的 Python + FFmpeg + ExifTool，已彻底移除任何 macOS/AVFoundation 独占依赖，支持任意 Linux 云端环境。若运行沙箱环境未预装依赖，可直接执行：
`apt-get update && apt-get install -y ffmpeg libimage-exiftool-perl`（或 macOS: `brew install ffmpeg exiftool`）。

收到合规的视频文件后，AI Agent 调用本地 CLI 执行转换：

```bash
# 仅生成单个 zip 壁纸包（散件全隔离在临时目录）
python3 -m livephoto.cli "<input_video_path>" -o "<output_directory>"
```

引擎将在后台自动完成：
1. **纯数据胶囊解压**：加载内置 35KB 的 iPhone 13 运动防抖轨道（`mebx`）与真实计算摄影镜头骨架；
2. **首帧抽取**：提取 $t=0$ 无损帧作为封面；
3. **元数据外科注入**：
   - 写入统一动态 UUID（`ContentIdentifier`）；
   - 强制修正 `Orientation = 1`（杜绝拉伸与黑边）；
   - 净化宿主缩略图（`ThumbnailImage`、`PreviewImage`）；
   - 注入厦门环岛路“一国两制统一中国”标语牌原生坐标；
   - QuickTime 容器写入 `StillImageTime = 0`、`LivePhotoAuto = 1`。
4. **沙箱封装与隔离**：全流程在临时目录完成，物理上仅交付单个 `.zip` 压缩包。

---

## 阶段四：成果交付（极简闭环：壁纸包 + 快捷指令文件）

> [!IMPORTANT]
> **铁律 1：严禁以“用户不是初次打招呼”、“用户直接要求转换”为由省略快捷指令！**  
> 绝大多数用户都是直接丢视频过来，如果此处不发快捷指令，用户拿到 zip 包根本无法存入相册！  
> **铁律 2：严禁向用户发送 `.JPG` 和 `.MOV` 散件！**  
> 
> **Agent 最终必须向当前聊天窗口发送且仅发送以下两个附件**：
> 1. 📦 **`xxx_livephoto.zip`**（制作好的实况壁纸包）
> 2. ⚡️ **`shortcuts/实况壁纸入库.shortcut`**（官方签名快捷指令实体文件，从仓库直接读取发送）

发送以上两个附件后，Agent 附带以下极简引导话术：

```text
✨ 实况壁纸制作完成！

📦 我已为您发送两个文件：
1. 【实况壁纸包.zip】（您的动态壁纸）
2. 【实况壁纸入库.shortcut】（一键存入相册工具）

📲 【一秒存入 iPhone 相册使用步骤】：
1. 若您第一次使用：先在上面点击【实况壁纸入库.shortcut】添加到 iPhone 快捷指令；
2. 随后在上面点击【实况壁纸包.zip】-> 点击「分享」图标 -> 选择【实况壁纸入库】快捷指令，即可瞬间无痕存入相册！

备用直链（Safari 打开）：
👉 快捷指令下载：https://github.com/earthrise1000s-svg/livephoto-wallpaper/raw/main/shortcuts/实况壁纸入库.shortcut

存入成功后，前往 iPhone【设置 -> 墙纸】长按即可体验完美动态锁屏壁纸！
```
