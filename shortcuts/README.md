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

## ⚙️ 快捷指令内部完整动作链（智能双模架构）

本快捷指令已预置智能双模分支，自适应网络链接与本地文件两种场景，零报错闭环：

```text
1. 接收输入 (URL 文本、网络链接 或 本地 ZIP 文件)
       │
       ▼
2. 识别链接 (is.workflow.actions.detect.link)
       │
   ┌───┴───────────────────────────────┐
   ▼                                   ▼
【分支 A：检测到 URL 链接】        【分支 B：本地已下载的 ZIP 文件】
自动调用 downloadurl 下载压缩包    直接读取传入的 ZIP 文件实体
   │                                   │
   └───────────────┬───────────────────┘
                   ▼
3. 解压实况 Bundle (is.workflow.actions.unarchive)
   (自动识别并解压出 .pvt/ 苹果原生实况包与配对 .JPG/.MOV)
                   │
                   ▼
4. 存入系统相册 (is.workflow.actions.savetocameraroll)
   (识别 com.apple.live-photo 类型，原子级存入相册)
                   │
                   ▼
5. 成功通知提醒 (is.workflow.actions.notification)
   (弹窗提示：“实况壁纸入库成功 🎉，已存入相册，可前往【设置 -> 墙纸】应用”)
```

---

## 🔗 自动化呼起 Magic Link

AI Agent 在生成实况壁纸压缩包后，可通过 Safari 打开如下协议链接，自动触发已安装的快捷指令并完成入库：

```text
shortcuts://run-shortcut?name=实况壁纸入库&input=text&text=<ZIP_DIRECT_URL>
```

无论是在手机聊天窗口直接轻点上述 Magic Link，还是把 ZIP 文件下载到本地后点击「分享」选择快捷指令，两种方式均已 100% 完美支持！
