---
worker_id: level-specialist-03-acceptance
stage: 5
role: level-specialist
level: bdd_scenarios
status: complete
blockers: []
confidence: high
---

# 行为场景

依据：`../final_specs/spec.md`；与 `acceptance_criteria.md` 配套，描述用户行为，未执行测试。同一真实 worker 编写两个紧密相关层级。Windows 原生 Tk 与实际 CLI 为两个验收入口，真实 Tk 控件和事件循环替代 Web 浏览器验收。

```gherkin
Feature: 用户只下载指定单视频
  Scenario Outline: BDD-01 支持单视频链接
    Given 用户打开窗口并选择可写目录
    When 粘贴 <链接形态> 并下载
    Then 只产生所指定视频的媒体文件
    Examples:
      | 链接形态                        |
      | youtube.com/watch?v=有效ID       |
      | youtube.com/shorts/有效ID        |
      | youtube.com/live/有效ID          |
      | youtube.com/embed/有效ID         |
      | youtu.be/有效ID                  |
      | watch?v=有效ID&list=有效列表ID    |

  Scenario Outline: BDD-02 错误输入不会开始下载
    Given 用户在窗口或 CLI 准备下载
    When 提交 <错误输入>
    Then 用户得到输入错误、保存目录无新增媒体且无网络调用
    Examples:
      | 错误输入                             |
      | youtube.com.evil.example 的 watch URL |
      | file 或 ftp URL                      |
      | https://user:pass@youtube.com/watch   |
      | 纯 playlist 或频道 URL               |
      | watch 缺少 v 或 v 的 ID 无效          |

Feature: 用户看见可信状态与适合的文件
  Scenario Outline: BDD-03 选择输出形式
    Given 一个公开可访问的单视频
    When 选择 <模式> 并完成下载
    Then 最终文件符合 <结果> 且 ffprobe 能读取
    Examples:
      | 模式                      | 结果                         |
      | 最佳                      | 可用最佳视频 MP4             |
      | 2160/1440/1080/720/480     | MP4 高度不超过选择值         |
      | MP3                       | 只有音频、无视频流的 MP3     |

  Scenario: BDD-04 进度到完成
    Given 用户通过真实 Tk 控件启动下载
    When 下载和后处理运行
    Then 窗口继续响应并显示进度、可用速度/剩余时间和后处理日志
      And 直到进程成功且最终文件存在才显示完成和路径

  Scenario Outline: BDD-05 错误可见且可恢复
    Given 下载发生 <故障>
    When 任务结束
    Then 窗口显示错误而非完成并允许用户修正后重试
      And CLI 给出错误并返回非零状态
    Examples:
      | 故障                         |
      | 网络失败或视频不可访问       |
      | 下载/后处理进程失败          |
      | 进程成功但最终文件缺失       |
      | FFmpeg/ffprobe/JS 运行时缺失 |

Feature: 用户保留已完成工作并控制任务
  Scenario: BDD-06 取消后重试续传
    Given 下载产生了部分分片
    When 点击取消后以相同链接、格式和目录重试
    Then 分片保留并可用于续传，最终输出有效媒体
      And 取消期间不显示完成且不影响其他会话进程

  Scenario: BDD-07 关闭窗口与 CLI 中断
    Given 一个任务正在运行
    When 关闭窗口或在 CLI 按 Ctrl+C
    Then 仅该任务及其子进程终止并保留分片
      And CLI 中断返回非零状态

  Scenario: BDD-08 已完成文件受保护
    Given 该目录已有完整下载文件
    When 重复下载同一视频和格式
    Then 原文件哈希不变

Feature: 登录与本机配置由用户控制
  Scenario Outline: BDD-09 登录选择
    Given 用户选择 <浏览器>
    When 开始下载
    Then cookies 行为为 <行为>
      And 读取失败时错误可见，不切换到其他浏览器
    Examples:
      | 浏览器  | 行为                         |
      | 未选择  | 不读取浏览器 cookies         |
      | Chrome  | 只读取显式选定 Chrome cookies |
      | Edge    | 只读取显式选定 Edge cookies   |
      | Firefox | 只读取显式选定 Firefox cookies |

  Scenario: BDD-10 用户配置不改变单视频任务
    Given 本机 yt-dlp 用户配置启用了整表下载和外部命令
    When 窗口或 CLI 下载一个合法单视频
    Then 仅下载单视频且配置中的外部命令不执行
```

真实网络、浏览器 cookies 与人工观感单独记录执行证据；离线边界案例不能替代实际下载黄金路径。整频道/整表下载、平台集成、服务部署及无权限视频成功下载不在验收门内，交主代理统一展示范围；保留其拒绝与失败路径测试。
