## 人工补充（代理 2026-11-04，按独立审片 qc.md 修改后；上传前用户核对）

### 两个版本选哪个

- 默认母版 `render/ep13_tallest_statues_master.mp4`：41 张卡里 32 张有图，其中 9 张是 Codex 生成的写实插画（中国 6、泰国 2、墨西哥 1，这几国的雕塑都在全景自由覆盖范围内；卡上标 AI IMAGE，署名写 AI-generated），**上传时「Altered or synthetic content」选 Yes**；另 9 张为占位（日本 5、台湾 1、缅甸 1、印尼 1、菲律宾 1，原因写「licence unclear」）。上面的描述框与置顶评论对应这一版。
- 风险版 `render/ep13_tallest_statues_master_with-risk-images.mp4`：41 张卡全部有图，其中 18 张来自新闻 / 博客 / 旅游网站、许可不明（已剔除来源页明写 All rights reserved 的图）。**选它须用户签字**，并把描述框「Image credits」换成下面这一段、置顶评论用 `_build/publish_risk_generated.md` 的 Comment 1。
- 两版都含雕塑版权（FoP）风险项：俄罗斯、乌克兰、塞内加尔、印尼、菲律宾、越南的雕像（详见 `sources.md` §3 与 qc.md 的分级），须用户逐项签字。

### 风险版 Image credits（替换描述框同名段落）

```text
Image credits (resized and cropped, no other changes; 2 images marked AI-generated are illustrations, not photos):
#1 Statue of Unity: Ronak Davda (Unsplash License)
#2 Laykyun Sekkya: McKay Savage (CC BY 2.0)
#3 Spring Temple Buddha: Gary Todd (CC0 1.0)
#4 Ushiku Daibutsu: Ganesh photography (Pexels License)
#5 Guishan Guanyin: William Chen (Pexels License)
#6 Sendai Daikannon: Ryne Anderson (Unsplash License)
#6 Great Buddha of Thailand: Valeria Drozdova (Pexels License)
#8 Hokkaido Kannon: Stuart Rankin (CC BY 2.0)
#9 The Motherland Calls: Eduardo Gómez (Unsplash License)
#10 Ksitigarbha of Jiuhua: CharlotteWhite (uploader; photographer not separately credited) (unknown)
#11 Grand Buddha at Lingshan: Boris Kasimov (CC BY 2.0)
#12 Statue of Belief: Bigul Malayi (CC0)
#13 Guanyin of Nanshan: Gary Todd (CC0 1.0)
#14 Kyaikhto Seated Buddha: unknown (unknown)
#15 Garuda Wisnu Kencana: Fiqih Alfarish (Unsplash License)
#15 Phra Buddha Chok: บ้านเรา"เขาวงพระจันทร์" ลพบุรี (credited image provider) (unknown)
#17 Kaga Kannon: ゲル / geruart25 (unknown)
#18 Confucius of Mount Ni: 老朱陪你看世界 (publisher; photographer unconfirmed) (unknown)
#19 Leshan Giant Buddha: Eleonora Costi (unknown)
#20 Wat Paknam Great Buddha: Teodor Kuduschiev (Unsplash License)
#21 Lady Buddha of Son Tra: Khang Too (Pexels License)
#22 Yang'asha Statue: unknown (unknown)
#23 Kurume Jibo Kannon: ao2222 (unknown)
#23 Mother Ukraine: Ev Vekselman (Pexels License)
#25 Guanyin of Mount Xiqiao: Mehmet Turgut Kirkgoz (Pexels License)
#26 Guan Yu of Yuncheng: unknown (unknown)
#26 Jesus of Sibea-bea: @ma_gints / Instagram (unknown)
#28 Mukdahan Great Buddha: unknown (unknown)
#29 Luang Pho Yai: icon0 com (Public domain (PublicDomainPictures.net, 'Free public domain image'))
#30 God of Red Mountain: AI-generated (AI-generated (Codex image_gen))
#31 Aizu Jibo Kannon: S.KOBAYASHI (unknown)
#32 Emei Maitreya Buddha: 曾 成訓 (CC BY 2.0)
#33 Tokyo Bay Kannon: unknown (unknown)
#34 The Victor: JG Summit Holdings (unknown)
#35 Buddha Dordenma: Unma Desai (Unsplash License)
#36 Koxinga Statue: Alexander Synaptic (unknown)
#37 Emperors Yan and Huang: AI-generated (AI-generated (Codex image_gen))
#38 Usami Daikannon: tukamen (unknown)
#38 Shodoshima Daikannon: unknown (unknown)
#38 Guerrero Chimalli: Guerrero Chimalli (Facebook page) (unknown)
#41 African Renaissance: Omoniyi David (Unsplash License)
CC BY 2.0 licence: https://creativecommons.org/licenses/by/2.0/
```

### 标签（tags）

```text
tallest statues, tallest statues in the world, world's tallest statue, statue of unity, spring temple buddha, laykyun sekkya, ushiku daibutsu, motherland calls, statue of liberty, biggest statues, giant buddha, top 41, ranking, data comparison, 2026
```

### 置顶评论开头（加在 Comment 1 最前面）

```text
How we measured: the statue itself, not its pedestal or throne. That's why Spring Temple Buddha is 108 m here (128 m includes its 20 m lotus throne) and the Statue of Belief is 78.9 m (its 112 m includes a 34 m pedestal). Some cards use clearly labelled AI-generated illustrations where no freely licensed photo exists.
Not included because the figure's own height isn't published or sources conflict: Mother of All Asia (Philippines), Tsz Shan Guanyin (Hong Kong), Khai Nguyen Amitabha and Ba Den Bodhisattva (Vietnam), Chiang Rai Guanyin, Lung Por Tuad and Phra Kakusunto (Thailand), Taihu Guanyin and Fo Guang Big Buddha. Details: see Comment 2 / the sources file. Spot a number you think is wrong? Reply with a source.
```

### 其他

- 无配乐（静音母版），配乐由主代理统一做后重渲。
- Luang Pho Yai 的 PublicDomainPictures.net 许可页本机打不开（403），发布前请点开确认「public domain」字样。
