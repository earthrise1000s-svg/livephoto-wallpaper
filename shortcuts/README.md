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

## ⚙️ 快捷指令内部完整动作链

本快捷指令已预置完整的自动化执行逻辑，无需手动组装：

```text
1. 接收输入 (接收 AI Agent 传入的 URL 或 Zip 文件)
       │
       ▼
2. 识别链接 (is.workflow.actions.detect.link)
       │
       ▼
3. 下载实况压缩包 (is.workflow.actions.downloadurl)
       │
       ▼
4. 解压实况 Bundle (is.workflow.actions.unarchive)
   (自动释放 .pvt/ 苹果原生实况包与配对 .JPG/.MOV)
       │
       ▼
5. 存入系统相册 (is.workflow.actions.savetocameraroll)
   (识别 com.apple.live-photo 类型，原子级存入相册)
       │
       ▼
6. 成功通知提醒 (is.workflow.actions.notification)
   (提示用户已成功入库，可前往锁屏设置应用动态壁纸)
```

---

## 🔗 自动化呼起 Magic Link

AI Agent 在生成实况壁纸压缩包后，可通过 Safari 打开如下协议链接，自动触发已安装的快捷指令并完成入库：

```text
shortcuts://run-shortcut?name=实况壁纸入库&input=text&text=<ZIP_DIRECT_URL>
```
