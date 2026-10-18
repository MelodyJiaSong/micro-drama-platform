# 审核：ep1_s3_st3 · 20261018-115103_fa9b104e

状态：不选（锤在左肩，由 20261018-122756_d24aad3c 替代）

Vision：满足。亚伦从好的一边架起维里，维里说清要去哪、为什么急，两人朝修道院赶。

## 对的

- 朝向：从首帧图开始，河在画左、木栅在画右（朝南看来路），两人朝镜头走＝往北去修道院，与 st1、st2 一致——前一条镜像的问题解决了。
- 伤在维里右上臂（他在画左，伤臂垂在画左外侧、血往下滴），亚伦在画右，维里把没受伤的左臂搭上亚伦的肩；台词逐字对（faster-whisper：「You're bleeding. Here, lean on me. / Get me to the Abbey. Brother Samuel can stop the bleeding. And there's a woman trapped in the vineyard. Hurry. / I'm going to the Abbey too. Come on.」）。15.07 秒。
- 最后两人朝镜头走来、擦过镜头出画。锤斜背，阴天湿路。

## 不对的

- 锤换了肩（另一会话拼整集时发现，6 秒抽帧核对属实）：两人面朝镜头时，锤头在亚伦头的画右＝他的**左**肩后，三视图与 st2 背影都是右肩。原因：维里的左臂要搭过亚伦的右肩，模型把锤挪到了另一边；首帧图里锤头也已在画右。

## 结论

选这条。之前的 100143 / 101818 / 104709 / 113926 都不用，保留不删。

## 怎么看的

1 fps 拼图，对照首帧图；faster-whisper small。
