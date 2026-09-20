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

## 阶段三：引擎执行与数据注入

收到合规的视频文件后，AI Agent 调用本地 CLI 执行转换：

```bash
# 默认生成配对文件与 zip 压缩包
python3 -m livephoto.cli "<input_video_path>" -o "<output_directory>" -z
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

---

## 阶段四：成果交付与二次引导闭环

合成完成后，Agent 必须根据用户在阶段一的选择提供针对性交付体验：

### 场景 A：用户已添加快捷指令（丝滑一键入相册）
```text
✨ 您的原生实况壁纸已制作完成！
- 封面图：[查看 JPG 封面](file:///path/to/IMG.JPG)
- 视频轨：[查看 MOV 视频](file:///path/to/IMG.MOV)

👉 点击下方链接一键保存到iPhone相册：
[【一键导入手机相册】](shortcuts://run-shortcut?name=实况壁纸入库&input=text&text=<ZIP_URL>)
```

### 场景 B：用户选择“暂不添加”（兜底安全警示）
```text
✨ 您的原生实况壁纸已制作完成！
- 压缩包下载：[点击下载实况壁纸包 (Zip)](file:///path/to/IMG_livephoto.zip)
- 独立文件下载：[JPG 封面](file:///path/to/IMG.JPG) | [MOV 视频](file:///path/to/IMG.MOV)

👉 [点此下载【实况壁纸入库】快捷指令一键保存](https://github.com/earthrise1000s-svg/livephoto-wallpaper/raw/main/shortcuts/实况壁纸入库.shortcut)

⚠️ 重要提醒：
若手动将 JPG 和 MOV 分别单独保存到手机相册，会被 iOS 识别为两份独立的普通文件，无法触发锁屏动态壁纸效果！强烈建议使用快捷指令一键入库。
```
