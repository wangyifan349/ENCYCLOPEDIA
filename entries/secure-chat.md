# 主要加密通信软件介绍🔒✨ 

## Signal 📲  
- 协议  
  • Signal Protocol（Double Ratchet、X3DH、AES-256-GCM、HKDF）  
- 注册方式  
  • 必须使用手机号注册，服务器仅保留注册手机号与上次连接时间🔑  
- 支持平台  
  • Android、iOS、Windows、macOS、Linux💻  
- 核心功能  
  • 一对一/群组文字、语音/视频通话、文件传输、消失消息🗑️、屏幕安全🛡️  
- 隐私特点  
  • 元数据最小化，不关联真实身份；客户端/服务器完全开源📜  

## Session 🕵️‍♂️  
- 协议  
  • 基于 Oxen Network 的 Lokinet（混淆流量、匿名 IP）+ Signal 风格加密🔗  
- 注册方式  
  • 完全匿名，无需手机号或邮箱，使用 66 字节 Session ID🆔  
- 支持平台  
  • Android、iOS、Windows、macOS、Linux📱🖥️  
- 核心功能  
  • 一对一/群组文字、语音消息、文件传输📂；可自定义“标签”群聊🏷️  
- 隐私特点  
  • 去中心化架构，无单点服务器；流量多层加密🛡️；客户端与节点代码开源  

## Tox 🐸  
- 协议  
  • 自研 Tox 协议，P2P+DHT，使用 libsodium 端到端加密🔐  
- 注册方式  
  • 无需注册，自动生成公私钥对，通过 Tox ID 加好友🔗  
- 支持平台  
  • Windows、macOS、Linux、Android（部分客户端）📀  
- 核心功能  
  • 一对一/群组文字、语音/视频通话、屏幕共享🎥、文件传输📁  
- 隐私特点  
  • 真正 P2P，无中心服务器；消息直连端到端；完全开源🌐  

## Jami 👐  
- 协议  
  • RING 分布式协议（P2P + DHT + NAT 穿透）🔄  
- 注册方式  
  • 无需账号，生成设备指纹作为标识🔑  
- 支持平台  
  • Windows、macOS、Linux、Android、iOS📱💻  
- 核心功能  
  • 一对一/群组文字、语音/视频通话、屏幕共享🖥️、文件传输📂、会议模式👥  
- 隐私特点  
  • 去中心化，无账户服务器；消息端到端加密；协议与客户端开源🎉  

## Element 🌐  
- 协议  
  • Matrix（Olm/Megolm 端到端加密）🔏  
- 注册方式  
  • 邮箱/手机号注册官方服务器，或自建 Matrix 服务器📧  
- 支持平台  
  • Web、Windows、macOS、Linux、Android、iOS🖥️📱  
- 核心功能  
  • 一对一/群组文字、文件、语音/视频通话📞、协作白板📝、多种桥接🤝  
- 隐私特点  
  • 联邦式模型，可自建服务器掌控数据；端到端加密需客户端开启🔒  

## Wire 🤝  
- 协议  
  • Proteus（Double Ratchet、2048-bit DH、AES-GCM、HKDF）  
- 注册方式  
  • 邮箱/手机号注册（企业版支持 SSO/SCIM）📧  
- 支持平台  
  • Web、Windows、macOS、Linux、Android、iOS💼  
- 核心功能  
  • 一对一/群组文字、语音/视频通话、屏幕共享🖥️、团队协作工具📊  
- 隐私特点  
  • 端到端加密；企业版支持审计与保留策略；客户端开源、服务器闭源🔍  

## Ricochet 🕳️  
- 协议  
  • Tor 隐蔽服务（.onion），本地启动 Tor 进程🧅  
- 注册方式  
  • 无需注册，生成 .onion 地址互加好友🔗  
- 支持平台  
  • Windows、macOS、Linux💽  
- 核心功能  
  • 一对一纯文字聊天✉️  
- 隐私特点  
  • 全流量通过 Tor 多层匿名；无中心服务器；客户端开源🔓  

## Silence 📬  
- 协议  
  • Signal Protocol over SMS/MMS📲  
- 注册方式  
  • 使用本机 SIM 卡号码，无需网络🌐  
- 支持平台  
  • Android📱  
- 核心功能  
  • 一对一加密短信（含图片/视频）🖼️；不支持语音或大文件  
- 隐私特点  
  • 本地端到端加密；运营商仅见密文；完全离线；客户端开源🔏
