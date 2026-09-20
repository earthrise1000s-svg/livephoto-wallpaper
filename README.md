# LivePhoto-Wallpaper 📸✨

> **视频转iphone可识别动态壁纸**  
> 100% 完美支持 iOS 17+ 锁屏动态壁纸的原生 Live Photo。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![iOS Tested](https://img.shields.io/badge/iOS-27%20Tested-success.svg)](https://apple.com/ios)
[![Zero External Assets](https://img.shields.io/badge/Assets-Zero%20Dependency%20(Pure%20Capsule)-brightgreen.svg)](#)

[English Documentation](README_EN.md) | [中文说明](README.md)

---

## 🌟 核心痛点与攻克原理

### 为什么同样是 iPhone 拍的 Live 图，有的能做动态壁纸，有的却不行？

很多苹果用户都会遇到这个奇怪的现象：明明都是用 iPhone 拍的原生实况照片，在相册里长按都能动，但只要一设成锁屏壁纸，有的就能流畅播放，有的却被提示“此实况照片不可用”！

原因主要有三：

- **画面太晃直接被关掉（苹果的“防晕车”保护机制）**，只有拍摄极其平稳、动作流畅的 Live 图才会被放行。
- **封面图和视频开头没对齐（杜绝画面跳闪）**，苹果只要检测到封面和第 0 帧没有严丝合缝，就会直接罢工。
- **缺失了关键的“陀螺仪防抖数据”**，普通工具合成的实况图根本没有这层数据。

---

### 💡 本工具是干什么的？

无论你给的是什么视频（自己拍的短片、动漫片段、电影剪辑等）：  
本工具会自动为它**无缝注入一份3秒长的手持极稳、平滑完美的 iPhone 原厂参数的 live photo**，让苹果锁屏系统 100% 坚信**“这是一张极平稳的原厂优质实况照片”**，完美激活锁屏长按动态效果！

---

## 📊 方案对比

| 核心特性 | 普通第三方转换工具 / App | 传统开源脚本 | **LivePhoto-Wallpaper (本项目)** |
| :--- | :---: | :---: | :---: |
| **iOS 17+ 锁屏动态壁纸支持** | ❌ 经常失效 / 提示不支持 | ⚠️ 部分支持但偶发拉伸 | **✅ 100% 原生识别、流畅播放** |
| **外部素材依赖** | 需下载专用宿主模板 | 需手动准备特定 iPhone Live 图 | **✅ 零依赖！内置 25KB 纯数据胶囊** |
| **视频画质损耗** | ⚠️ 二次重编码压制降质 | ⚠️ 重新编码 | **✅ Passthrough 流复制，画质零损耗** |
| **方向与黑边处理** | ❌ 容易竖变横或产生黑边 | ⚠️ 需手动配置参数 | **✅ 强制归一 Orientation=1，自动适应宽高** |
| **手机相册一键导入** | 需在 App 内部繁琐保存 | 需手动 AirDrop / 分离保存 | **✅ 配套快捷指令 Magic Link 一键入库** |
| **AI Agent / CLI 适配** | ❌ 仅限图形界面 | ⚠️ 接口杂乱 | **✅ 开箱即用 CLI + 标准化 SKILL.md** |

---

## 🚀 两种使用方式（按需选择）

### 方式 A：📱 AI Agent手机聊天端使用（普通用户首选！）

如果您是通过各类 AI Agent 客户端使用本工具，**您完全不需要在手机上敲任何命令或安装任何运行环境**，底层转换由后台 AI 自动完成：

1. **添加配套快捷指令（仅需一次）**：  
   在 iPhone 上点击下载并添加官方签名指令 👉 **[【实况壁纸入库】快捷指令](https://github.com/earthrise1000s-svg/livephoto-wallpaper/raw/main/shortcuts/实况壁纸入库.shortcut)**（用于后续将制作完成的文件一键无痕存入相册）；
2. **发送目标视频**：  
   在聊天窗口中直接发送您想制作为锁屏壁纸的**视频文件**（若是相册现有的实况图，请先在相册点击右上角 `...` 选择【存储为视频】后再发）；
3. **一键存入相册**：  
   AI制作完成后会提供一键链接，点击即可自动唤起快捷指令，瞬间将配对的 Live Photo 存入相册！

---

### 方式 B：💻 开发者 / 本地终端调用（用于本地批量处理或二次开发）

如果您是开发者或希望在 Mac / Linux 电脑本地通过终端命令行进行批量处理：

1. **环境准备（仅开发者需要）**：
   ```bash
   # macOS 安装 exiftool
   brew install exiftool
   ```

2. **克隆与安装**：
   ```bash
   git clone https://github.com/earthrise1000s-svg/livephoto-wallpaper.git
   cd livephoto-wallpaper
   pip install .
   ```

---

## ❓ 常见问题 (FAQ)

### Q1: 我可以直接上传现有的 Live 图来制作吗？
**答：建议先导出为视频！**  
在 iPhone 端如果直接在聊天软件或网页中选中实况照片上传，系统默认**只会发送静态的 JPG 封面**，底层视频数据会被直接丢弃。  
**正确做法**：在 iPhone「照片」中打开该实况图，点击右上角 `...` 菜单，选择 **【存储为视频】**，将导出的视频交给本工具即可重新合成为完美支持锁屏的实况壁纸！


---

## 📄 开源许可证

本项目采用 [MIT License](LICENSE) 开源。欢迎 Star、Fork 与提交 Issue！
