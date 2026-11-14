# k751 Burrowstrike · follow-up 301 续（10 秒，时间轴 771b7acfd788）

- 任务 `5358b638`，168 积分，720p，10.08 s。改法（用户）：先对打、尖刺带不规则倒钩骨刺、瞬出瞬收、树人落地即死。开场图 `planning/k751_start_v301f.png`、峰值图 `planning/k751_peak_v301b.png`（同机位尖刺炸出一刻）、树人死亡样板。出片前闸门 locked_traits / scale / gaze / status_visual 用户放行。
- 前一次提交 `ac48ba61` 服务端 `code=1151 TranscodeFail` 无产出，按同一资料包重提；本条下载三次不完整，`poll` 重下成功，没有重提。

## 流畅自检
- `motion_check --action 1.5-8.5`：中位 175，无慢动作嫌疑或定格；无剪切。

## 代理看拼图与放大帧
- 尖刺终于对：狰狞的倒钩骨刺、凌厉，不再像宝塔；三个树人被弹上半空；它在右侧钻出时树人还在空中；结尾树尸躺地、尘土落定；1.5–4.75 s 对打积极。
- 偏差：第一帧蝎子偏大、左边被切；尖刺 6.25–7.25 s 立约 1 s，没做到瞬间收回；钻出约 7 s（计划 6.1–6.3 s）；树尸偏小偏暗、不好逐具辨认。

## 出片后多视角审稿（qc.json）— 闸门不通过
- 实打实：timeline / agency / attack_tempo（地下与尖刺段拖长、钻出晚）、head_tail / subject_count（首帧被切、结尾树尸认不清）。
- fidelity 审稿人说尖刺像「细长塔状」——放大帧看已是带倒钩的不规则骨刺，判审稿误读，交用户看。
- 其余多为拼图太小「拿不准」：scale、gaze、readability、attack_contact。
- 声音未核听。未锁片；已拼进 demo v5 供整体看。
