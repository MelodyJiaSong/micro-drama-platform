---
worker_id: level-specialist-03-acceptance
stage: 5
role: level-specialist
level: acceptance_criteria
status: complete
blockers: []
confidence: high
---

# 验收标准

依据：`../final_specs/spec.md`。本文件定义验收契约，未执行测试。窗口验收必须启动真实 Tk 事件循环、驱动可见控件并运行实际下载进程；CLI 入口单独验证。没有 Web 服务、API 或浏览器运行模式。自动化通过后仍须人工查看窗口、焦点、进度可读性，并在用户网络环境试用。

```gherkin
Feature: Windows 单视频下载

  Scenario: AC-01 原生窗口黄金路径与进度
    Given 项目自己的 .venv 已安装依赖且下载所需工具齐备
      And 一个可访问的 YouTube 单视频及可写保存目录
    When 用户启动窗口并粘贴链接、选择目录和清晰度后点击下载
    Then 窗口显示下载进度、可用的速度和剩余时间以及后处理日志
      And Tk 事件循环持续响应且同一窗口不能启动第二个并行任务
      And 下载进程成功且最终 MP4 文件存在后才显示完成与最终路径
      And ffprobe 能读取最终文件并识别视频流

  Scenario Outline: AC-02 视频清晰度上限
    Given 源视频有多种可用分辨率
    When 用户选择 <上限> 并完成下载
    Then 最终 MP4 视频高度不超过 <上限>
      And 源格式不足时使用可用格式而不承诺达到所选高度
    Examples:
      | 上限 |
      | 2160 |
      | 1440 |
      | 1080 |
      | 720  |
      | 480  |

  Scenario: AC-03 最佳格式与 MP3
    Given 一个有视频与音频的可访问单视频
    When 用户分别以最佳视频和 MP3 模式下载到独立目录
    Then 最佳模式输出可由 ffprobe 读取的视频 MP4
      And MP3 模式的最终媒体文件是 MP3、含音频且无视频流
      And 两次任务均显示各自存在的最终文件路径

  Scenario Outline: AC-04 非法链接在外部调用前拒绝
    Given 用户使用 <入口>
    When 提交伪装域名、非 HTTP(S)、含账号密码、纯列表、频道、缺失或无效视频 ID 的链接
    Then 给出明确的链接错误且不启动下载或网络请求
      And CLI 入口返回非零状态
    Examples:
      | 入口 |
      | 窗口 |
      | CLI  |

  Scenario: AC-05 取消、关闭与续传
    Given 本任务正在下载且已产生分片，另有独立会话进程运行
    When 用户点击取消或关闭窗口
    Then 本任务及其子进程终止而独立会话继续运行
      And 已下载分片保留且不显示完成
    When 用户在同目录以相同链接和格式重试
    Then 工具可利用保留分片续传直至最终文件完成

  Scenario: AC-06 已存在文件不覆盖
    Given 保存目录已有该视频的完整输出并记录其哈希
    When 用户再次以相同模式下载
    Then 原文件内容和哈希不变
      And 界面如显示完成，其最终路径指向真实存在的文件

  Scenario Outline: AC-07 失败不冒充成功
    Given 任务遇到 <失败条件>
    When 用户下载并等待任务结束
    Then 保留并显示可理解的失败信息且不显示完成
      And 窗口恢复可操作状态，CLI 返回非零状态
    Examples:
      | 失败条件                  |
      | 视频不可访问或网络失败    |
      | 下载进程返回非零          |
      | 进程返回零但最终文件缺失  |
      | 浏览器 cookies 读取失败   |

  Scenario: AC-08 浏览器登录需显式选择
    Given 用户未选择浏览器
    When 开始下载
    Then 不读取任何浏览器 cookies
    When 用户显式选择 Chrome、Edge 或 Firefox 后开始新任务
    Then 仅请求该浏览器的 cookies
      And 读取失败时显示原有错误，不改用其他浏览器或显示成功

  Scenario: AC-09 安装提示与配置隔离
    Given 缺少 FFmpeg、ffprobe 或所需 JS 运行时
    When 启动下载
    Then 给出对应安装提示且不显示完成
    Given 用户的 yt-dlp 配置要求下载播放列表或执行外部命令
    When 下载一个合法单视频
    Then 用户配置不影响本任务，既不下载整表也不执行其配置命令

  Scenario: AC-10 CLI 成功及 Ctrl+C
    Given 与窗口相同的合法链接、目录和格式
    When 从实际 CLI 入口启动下载
    Then 成功时输出存在且可由 ffprobe 读取的最终路径并返回零状态
    When 下载途中用户按 Ctrl+C
    Then 本任务及其子进程停止、分片保留且返回非零状态
```

普通验收失败为 blocker；安全相关失败按安全层级判为 critical。实时网络不可用时明确标记受阻或跳过，保留离线集成结果，不能据此宣称真实下载验收通过。
