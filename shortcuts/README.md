# iOS 快捷指令配套方案 (100% 官方签名实装)

本仓库已完整内置由 Apple 原生安全签名验证的真实快捷指令文件：  
👉 **[点击直接下载【实况壁纸入库.shortcut】](https://github.com/earthrise1000s-svg/livephoto-wallpaper/raw/main/shortcuts/实况壁纸入库.shortcut)**（21KB，已完成 `shortcuts sign --mode anyone` 官方全局签名认证）

---

## 📱 安装方式（两选一）

### 方式 A：直接在 iPhone 点击下载文件（推荐，离线永久有效）
1. 在 iPhone Safari 浏览器中点击上方 👉 **[下载【实况壁纸入库.shortcut】](https://github.com/earthrise1000s-svg/livephoto-wallpaper/raw/main/shortcuts/实况壁纸入库.shortcut)**；
2. 系统会自动下载并呼起 Apple 官方「快捷指令」App，弹出 **【添加快捷指令】** 确认面板；
3. 点击添加即可完成安装。

### 方式 B：通过 iCloud 链接一键添加
若您在 Mac 快捷指令应用中右键该指令选择「共享 -> 拷贝 iCloud 链接」，即可获得专属在线分发链接。

---

## ⚙️ 快捷指令内部完整动作链（URL 全自动流式入库）

快捷指令采用纯 URL 驱动，**用户完全无需手动下载 ZIP 压缩包**，全流程在后台静默全自动完成：

```text
1. 接收输入 (接收 AI 提供的壁纸包 URL 链接)
       │
       ▼
2. 识别链接 (is.workflow.actions.detect.link)
       │
       ▼
3. 后台静默下载压缩包 (is.workflow.actions.downloadurl)
       │
       ▼
4. 自动解压实况 Bundle (is.workflow.actions.unarchive)
   (自动释放 .pvt/ 苹果原生实况包与配对 .JPG/.MOV)
       │
       ▼
5. 原子级存入系统相册 (is.workflow.actions.savetocameraroll)
   (识别 com.apple.live-photo 类型，直接写入相册底表)
       │
       ▼
6. 成功弹窗提示 (is.workflow.actions.notification)
   (弹窗提示：“实况壁纸入库成功 🎉，已存入相册，可前往【设置 -> 墙纸】应用”)
```

---

## 🔗 自动化呼起 Magic Link

AI Agent 生成实况壁纸包后，直接向用户提供专属唤醒链接。用户在 iPhone 轻点链接即可全自动入库：

```text
shortcuts://run-shortcut?name=实况壁纸入库&input=text&text=<ZIP_DIRECT_URL>
```

**极简闭环体验**：
- 用户**无需点击下载文件**；
- 用户**无需打开 iOS 文件 App**；
- 仅需在聊天窗口点击一下链接（或长按复制 URL 打开快捷指令），实况壁纸瞬间存入相册！
