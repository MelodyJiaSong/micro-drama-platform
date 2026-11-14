# -*- coding: utf-8 -*-
"""follow-up 016 第一步的浓缩：每项「长什么样、标志性视角、易混对象」→ image_hint（喂给 Codex）与 content/*.md。
look = 外观与辨认特征；view = 最佳拍摄视角 / 机位；avoid = 易混淆对象（要排除）。"""

H = {
 "Statue of Unity": dict(
    look="bronze-clad standing statue of Sardar Vallabhbhai Patel in a dhoti and shawl, hands at his sides, on a tall grey base by the Narmada river and Sardar Sarovar Dam",
    view="full figure head to base from the front or front-three-quarter, from the river bank or the approach bridge; sunset or clear sky",
    avoid="Statue of Equality (Hyderabad), Ambedkar statues, Statue of Prosperity (Bengaluru), small Patel statues"),
 "Laykyun Sekkya": dict(
    look="huge golden-yellow standing Buddha with red robe accents on a hill at Bodhi Tataung near Monywa, a giant reclining Buddha lies in front of it",
    view="full standing figure from below on the hill path, or a wide shot with the reclining Buddha in the foreground",
    avoid="the reclining Buddha alone, Kyaikhto seated Buddha, Shwedagon"),
 "Spring Temple Buddha": dict(
    look="gilded copper standing Vairocana Buddha on a huge lotus throne atop stepped pedestals and a long staircase on a hill in Lushan county, Henan (Foquan Temple, Yaoshan)",
    view="full statue including the lotus throne seen from the base of the stairs; clear sky",
    avoid="Ushiku Daibutsu (Japan, bronze-coloured), Lingshan Grand Buddha (Wuxi), Tian Tan Buddha (Hong Kong, seated)"),
 "Statue of Belief": dict(
    look="huge copper-coloured seated Shiva in meditation, holding a trident, with a snake around the neck, on Ganesh Tekri hill at Nathdwara, Rajasthan",
    view="full seated figure from the front, ideally at dusk with lighting or clear blue sky",
    avoid="Murudeshwar Shiva (sea, Karnataka), Adiyogi bust (Coimbatore), Kailashnath Mahadev (Nepal), Mangal Mahadev (Mauritius)"),
 "Ushiku Daibutsu": dict(
    look="standing bronze Amitabha Buddha with right hand raised, dark bronze colour, in a park with flower fields at Ushiku, Ibaraki, Japan",
    view="full figure from the front avenue or across seasonal flower beds (pink moss phlox / cosmos); clear sky",
    avoid="Spring Temple Buddha (gold, China), Kamakura Daibutsu (seated), Nara Daibutsu (indoor)"),
 "Guishan Guanyin": dict(
    look="gilded bronze thousand-armed, eleven-headed Guanyin on a hill (Pilu peak) behind Miyin Temple at Weishan, Ningxiang, Hunan; many arms fanned out",
    view="full statue from the plaza in front, showing the many gold arms",
    avoid="Nanshan Guanyin (white, sea), Tsz Shan Guanyin (white), other thousand-armed Guanyin indoors"),
 "Mother of All Asia": dict(
    look="huge white concrete statue of the Virgin Mary with hands joined, standing atop the Montemaria shrine hill in Batangas City, Philippines, overlooking Batangas Bay",
    view="full statue from the shrine grounds or a drone shot with the bay behind",
    avoid="other Marian statues, Virgen de la Paz (Venezuela), small grotto statues"),
 "Great Buddha of Thailand": dict(
    look="enormous gold-painted seated Buddha (Maravijaya pose, right hand touching the earth) at Wat Muang, Ang Thong; a pink/orange-roof temple below",
    view="frontal full view of the seated Buddha from the temple grounds, blue sky",
    avoid="Big Buddha Phuket (white marble), Wat Paknam Buddha (Bangkok), Phra Buddha Chok (Lopburi)"),
 "Sendai Daikannon": dict(
    look="all-white standing Kannon holding a water jar and a cintamani jewel, rising above a residential hillside in Izumi-ku, Sendai, Japan",
    view="full figure from below at the temple entrance, or a distant view over houses/forest",
    avoid="Hokkaido Kannon (Ashibetsu), Takasaki Byakui Kannon, Aizu Jibo Kannon"),
 "Hokkaido Kannon": dict(
    look="white Byakue Kannon with a tall headdress standing alone on a forested hill at Kita no Miyako park, Ashibetsu, Hokkaido",
    view="full statue from below with sky, or from the valley road; snow or green forest seasons",
    avoid="Sendai Daikannon, Takasaki Kannon, Usami Kannon (seated)"),
 "The Motherland Calls": dict(
    look="concrete woman striding forward, raising a long sword high, cloak billowing, on Mamayev Kurgan hill, Volgograd",
    view="full figure from the hill path below, sword visible, dramatic sky",
    avoid="Mother Ukraine (Kyiv, steel with shield), Alyosha (Murmansk), Rear-Front monument (Magnitogorsk)"),
 "Ksitigarbha of Jiuhua": dict(
    look="huge bronze standing Ksitigarbha (Dizang) monk with shaved head, holding a tall khakkhara staff in the right hand and a jewel in the left, on a lotus base at Dayuan Cultural Park, Mount Jiuhua, Anhui",
    view="full statue from the long axial plaza and stairs in front",
    avoid="Jiuhua mountain temples, Spring Temple Buddha, Lingshan Buddha"),
 "Grand Buddha at Lingshan": dict(
    look="bronze standing Amitabha Buddha with right hand raised, on a lotus base, on the southern slope of Lingshan hill near Taihu lake, Wuxi",
    view="full statue from the bottom of the long staircase (Bodhi Avenue), clear sky",
    avoid="Brahma Palace interior, Spring Temple Buddha, Nine Dragons bathing Buddha fountain"),
 "Guanyin of Nanshan": dict(
    look="white three-faced Guanyin statue standing on a man-made island in the sea off Sanya, Hainan, connected by a long bridge",
    view="full statue from the shore or bridge with sea and sky, or aerial; must show three faces / sea setting",
    avoid="Lady Buddha Da Nang, Tsz Shan Guanyin, Xiqiao Guanyin"),
 "Kyaikhto Seated Buddha": dict(
    look="huge gold seated Buddha at the Phayathonzu monastery near Kyaikhto, Mon State, Myanmar",
    view="frontal full view of the seated statue",
    avoid="Kyaiktiyo Golden Rock, Laykyun Sekkya standing Buddha, reclining Buddhas"),
 "Garuda Wisnu Kencana": dict(
    look="copper/brass Vishnu riding the eagle Garuda with huge outspread wings, atop a tall pedestal in GWK Cultural Park, Bali",
    view="full statue including wings, from the plaza below or an aerial view; clear sky",
    avoid="the older unfinished GWK head-only display, Garuda statue at Ngurah Rai airport roundabout"),
 "Phra Buddha Chok": dict(
    look="large gold-coloured seated Buddha on Khao Wong Phrachan mountain, Khok Samrong, Lopburi, Thailand",
    view="frontal full view of the seated Buddha against the mountain",
    avoid="Great Buddha of Thailand (Ang Thong), Wat Phra Phutthabat"),
 "Kaga Kannon": dict(
    look="white standing Kannon holding a baby, rising above the abandoned Kaga Kannon / Utopia Kaga resort in Kaga, Ishikawa, Japan",
    view="full figure from the road or field, distant shots fine",
    avoid="Kurume Jibo Kannon, Aizu Jibo Kannon"),
 "Khai Nguyen Amitabha": dict(
    look="giant standing Amitabha Buddha at Khai Nguyen Pagoda (Co Lieu), Son Tay, Hanoi",
    view="full figure from the pagoda grounds",
    avoid="Ba Den mountain Buddha (Tay Ninh), Bai Dinh pagoda statues"),
 "Confucius of Mount Ni": dict(
    look="huge bronze standing Confucius with hands folded, in scholar robes, at Nishan Shengjing park near Qufu, Shandong",
    view="full figure from the axial avenue, clear sky",
    avoid="small Confucius statues in Qufu temple, Confucius statues abroad"),
 "Leshan Giant Buddha": dict(
    look="giant seated stone Buddha carved into a red sandstone cliff at the confluence of the Min and Dadu rivers, Leshan, Sichuan; greenery on the cliff",
    view="full seated figure from the river (boat view) or from the stairway beside the statue, head to feet",
    avoid="Mengshan Buddha, Rongxian Buddha, Bamiyan"),
 "Tsz Shan Guanyin": dict(
    look="tall white bronze Guanyin holding a vase, on a lotus base at Tsz Shan Monastery, Tai Po, Hong Kong, with green hills",
    view="full figure from the courtyard in front, or from Plover Cove side",
    avoid="Tian Tan Buddha (Lantau, seated bronze), Nanshan Guanyin"),
 "Wat Paknam Great Buddha": dict(
    look="enormous gold seated Buddha behind Wat Paknam Bhasicharoen temple, Bangkok, next to a white stupa",
    view="frontal full view from the temple grounds, or along the canal",
    avoid="Wat Pho reclining Buddha, Great Buddha of Thailand (Ang Thong)"),
 "Lady Buddha of Son Tra": dict(
    look="white standing Quan Am (Lady Buddha) on a lotus base at Linh Ung Pagoda on Son Tra peninsula, Da Nang, facing the sea",
    view="full figure from below with blue sky, or with sea and city view",
    avoid="Linh Ung pagoda on Marble Mountains, Ba Na hills Buddha"),
 "Yang'asha Statue": dict(
    look="stainless-steel statue of the Miao goddess Yang'asha wearing silver headdress and holding a moon, on a round base by a river in Jianhe county, Guizhou",
    view="full figure from the riverside, silver metallic shine",
    avoid="other Miao village sculptures, silver jewelry close-ups"),
 "Mother Ukraine": dict(
    look="stainless-steel woman with sword raised and shield (now with Ukraine trident) on a tall museum base above the Dnipro, Kyiv",
    view="full figure with base from below or from across the park, sword and shield visible",
    avoid="The Motherland Calls (Volgograd, concrete), Mother Armenia, Kartlis Deda"),
 "Kurume Jibo Kannon": dict(
    look="white Kannon holding a child, at Naritasan Kurume temple, Kurume, Fukuoka",
    view="full figure from the temple grounds",
    avoid="Kaga Kannon, Aizu Jibo Kannon (also holds a child)"),
 "Guanyin of Mount Xiqiao": dict(
    look="huge bronze seated Guanyin on a lotus platform atop Xiqiao Mountain, Foshan, with long stairs leading up",
    view="frontal full view from the stairs / plaza below",
    avoid="Nanshan Guanyin (standing white), Guishan Guanyin"),
 "Jesus of Sibea-bea": dict(
    look="white Christ statue with outstretched arms standing above a serpentine switchback road on Sibea-bea hill near Lake Toba, Samosir, North Sumatra",
    view="full figure with the winding road below, aerial or from the road",
    avoid="Christ the Redeemer (Rio), Christ Blessing (Manado), Cristo Rei"),
 "Guan Yu of Yuncheng": dict(
    look="bronze standing Guan Yu with long beard holding a guandao glaive, on a high base near Changping village, Yuncheng, Shanxi",
    view="full figure from the plaza below, clear sky",
    avoid="Jingzhou Guan Yu (removed), Guan Yu temples, small Guan Yu statues"),
 "Mukdahan Great Buddha": dict(
    look="large white-and-gold seated Buddha on Phu Manorom hill, Mukdahan, Thailand, overlooking the Mekong",
    view="frontal full view of the seated statue",
    avoid="Phra That Phanom, other Isan Buddhas"),
 "Luang Pho Yai": dict(
    look="tall standing yellow Buddha in blessing posture at Wat Burapha Phiram, Roi Et city, Thailand",
    view="full figure from the temple grounds, blue sky",
    avoid="Roi Et tower, other standing Buddhas"),
 "God of Red Mountain": dict(
    look="huge bronze seated/standing sea god Chishan Mingshen at Chishan (Red Mountain) scenic area, Shidao, Rongcheng, Shandong",
    view="full statue from the plaza",
    avoid="Chishan Fahua temple buildings, Mazu statues"),
 "Aizu Jibo Kannon": dict(
    look="white Kannon holding a baby, at Aizumura park, Aizuwakamatsu, Fukushima, rising above trees",
    view="full figure from the park grounds",
    avoid="Kaga Kannon, Kurume Kannon"),
 "Emei Maitreya Buddha": dict(
    look="bronze standing Maitreya (smiling, round belly) above Emei Lake at Tian En Maitreya temple, Hsinchu County, Taiwan",
    view="distant full view across Emei Lake (the statue is not normally open), or from the lakeside trail",
    avoid="Fo Guang Shan Buddha, Changhua Great Buddha"),
 "Tokyo Bay Kannon": dict(
    look="white standing Kannon on Mt Otsubo hilltop in Futtsu, Chiba, looking over Tokyo Bay",
    view="full figure from below or distant from the bay side",
    avoid="Ofuna Kannon (bust), Nihonji Daibutsu"),
 "The Victor": dict(
    look="tall stainless-steel / silver-and-gold figure with both arms raised in triumph, beside the Bridgetowne bridge, Pasig, Metro Manila",
    view="full figure with the bridge and skyline, day or night lights",
    avoid="other public art in Bridgetowne"),
 "Buddha Dordenma": dict(
    look="gilded bronze seated Shakyamuni Buddha on the Kuensel Phodrang hill above Thimphu, Bhutan, on a temple base with golden female deity statues around the plaza",
    view="frontal full view from the plaza, blue sky and mountains",
    avoid="Tashichho Dzong, Punakha"),
 "Koxinga Statue": dict(
    look="large seated Zheng Chenggong (Koxinga) statue in armour at Xikou Kaiyuan temple, Chiayi County, Taiwan",
    view="frontal full view",
    avoid="Koxinga statue on Gulangyu (Xiamen), Koxinga shrine in Tainan"),
 "Emperors Yan and Huang": dict(
    look="two colossal stone busts of the Yan and Yellow Emperors carved on a hill facing the Yellow River at Zhengzhou, Henan",
    view="frontal view from the plaza below showing both heads",
    avoid="Yellow Emperor mausoleum (Shaanxi), small Yellow Emperor statues"),
 "Usami Daikannon": dict(
    look="white seated Kannon overlooking Usami / Ito on the Izu peninsula, Shizuoka",
    view="full seated figure",
    avoid="Tokyo Bay Kannon, Atami"),
 "Shodoshima Daikannon": dict(
    look="white standing Kannon at Shodoshima Daikannon temple on a hillside, Shodoshima island, Kagawa",
    view="full figure from the temple grounds or a distant hillside view",
    avoid="Olive park windmill, other Shodoshima temples"),
 "Guerrero Chimalli": dict(
    look="huge red stylised Aztec warrior with shield (chimalli) by sculptor Sebastián, on Av. Bordo de Xochiaca, Chimalhuacan, State of Mexico",
    view="full figure from the street or plaza, blue sky",
    avoid="other Sebastián sculptures (yellow horse 'El Caballito')"),
 "African Renaissance": dict(
    look="bronze group of a man holding a baby aloft with a woman, on a hill (Collines des Mamelles) at Ouakam, Dakar",
    view="full statue group from the bottom of the long staircase, sky behind",
    avoid="Dakar lighthouse (Phare des Mamelles)"),
}


def hint(name: str) -> str:
    h = H[name]
    return f"{h['look']}. Best view: {h['view']}. Exclude: {h['avoid']}"

# 第三轮补搜用的当地名称 / 别名（Codex 用当地语言搜图库、Flickr、旅游局图片库）
LOCAL = {
 "Spring Temple Buddha": "中原大佛, 鲁山大佛, 尧山大佛, 佛泉寺 (Foquan Temple)",
 "Laykyun Sekkya": "Laykyun Setkyar, Bodhi Tataung standing Buddha, Monywa",
 "Statue of Belief": "Vishwas Swaroopam, Nathdwara Shiva statue",
 "Guishan Guanyin": "沩山千手千眼观音, 密印寺观音, Weishan Guanyin",
 "Great Buddha of Thailand": "Wat Muang Ang Thong big Buddha, พระพุทธมหานวมินทร์ วัดม่วง",
 "Sendai Daikannon": "仙台大観音, 仙台天道白衣大観音",
 "Hokkaido Kannon": "北海道大観音, 芦別 北の京",
 "Ksitigarbha of Jiuhua": "九华山地藏菩萨露天铜像, 九华山大愿文化园, Jiuhuashan Ksitigarbha statue",
 "Grand Buddha at Lingshan": "灵山大佛, Lingshan Buddha Wuxi",
 "Guanyin of Nanshan": "南山海上观音, Nanshan Guanyin Sanya",
 "Kyaikhto Seated Buddha": "Kyaikhto big Buddha, Phayathonzu, ကျိုက်ထို",
 "Phra Buddha Chok": "พระพุทธโชค วัดเขาวงพระจันทร์",
 "Kaga Kannon": "加賀大観音, 加賀観音",
 "Confucius of Mount Ni": "尼山孔子像, 尼山圣境",
 "Leshan Giant Buddha": "乐山大佛",
 "Tsz Shan Guanyin": "慈山寺觀音",
 "Wat Paknam Great Buddha": "วัดปากน้ำภาษีเจริญ พระพุทธธรรมกายเทพมงคล",
 "Lady Buddha of Son Tra": "Quan Âm chùa Linh Ứng Sơn Trà",
 "Yang'asha Statue": "仰阿莎雕像, 剑河仰阿莎",
 "Mother Ukraine": "Батьківщина-мати, Мати-Україна, Motherland Monument Kyiv",
 "Kurume Jibo Kannon": "久留米 成田山 救世慈母大観音",
 "Guanyin of Mount Xiqiao": "西樵山南海观音, 西樵山观音像",
 "Jesus of Sibea-bea": "Patung Yesus Bukit Sibea-bea, Samosir",
 "Guan Yu of Yuncheng": "运城关公圣像, 常平关公像, 关公故里",
 "Mukdahan Great Buddha": "พระพุทธรูปภูมโนรมย์ มุกดาหาร, Phu Manorom",
 "Luang Pho Yai": "หลวงพ่อใหญ่ วัดบูรพาภิราม ร้อยเอ็ด",
 "God of Red Mountain": "赤山明神, 荣成赤山",
 "Aizu Jibo Kannon": "会津慈母大観音, 会津村",
 "Emei Maitreya Buddha": "峨眉湖 彌勒佛, 天恩彌勒佛院, 大自然文化世界",
 "Tokyo Bay Kannon": "東京湾観音, 富津",
 "The Victor": "The Victor Bridgetowne",
 "Buddha Dordenma": "Kuensel Phodrang Buddha Thimphu",
 "Koxinga Statue": "溪口 開元殿 鄭成功 雕像",
 "Emperors Yan and Huang": "炎黄二帝塑像, 郑州黄河风景区 炎黄",
 "Usami Daikannon": "宇佐美大観音, 伊東 宇佐美 観音",
 "Shodoshima Daikannon": "小豆島大観音",
 "Guerrero Chimalli": "Guerrero Chimalli Chimalhuacán",
 "African Renaissance": "Monument de la Renaissance africaine Dakar",
}


def hint(name: str) -> str:   # noqa: F811 —— 带当地名称的版本
    h = H[name]
    loc = f" Local names: {LOCAL[name]}." if name in LOCAL else ""
    return f"{h['look']}. Best view: {h['view']}. Exclude: {h['avoid']}.{loc}"
