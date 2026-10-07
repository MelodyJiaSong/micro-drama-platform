import hashlib
import json
import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.seedance_kit import Ref, validate_endpoint_characters


class EndpointKitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'planning').mkdir()
        self.md = self.root/'shot01.md'
        self.frames = [self.root/'first.png', self.root/'last.png']
        for n, path in enumerate(self.frames):
            path.write_bytes(f'approved endpoint {n}'.encode())
        self.refs = [Ref('start',self.frames[0],'图片',1), Ref('end',self.frames[1],'图片',2)]
        self.prompt = '角色: c1_Aaron青年；c2_Duke敦实青年'
        self.cards = ['c1_Aaron','c2_Duke']
        sources = []
        for card in self.cards:
            path = self.root/'characters'/card/'views.png'
            path.parent.mkdir(parents=True)
            path.write_bytes(card.encode())
            sources.append({**self.record(path),'character':card})
        self.contract = {'generation_mode':'first_last_frame','input_review':{'status':'passed'},
                         'terminal_framing':self.record(self.frames[1]),
                         'endpoint_control':{'first':self.record(self.frames[0]),'last':self.record(self.frames[1]),
                                             'characters':self.cards,'identity_sources':sources}}
        self.save()

    def record(self, path):
        return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'status':'passed'}

    def save(self):
        (self.root/'planning/continuous_take.json').write_text(json.dumps(self.contract),encoding='utf-8')

    def test_two_approved_frames_can_embed_verified_characters(self):
        validate_endpoint_characters(self.md,'',self.prompt,self.refs)

    def test_embedded_mode_cannot_drop_character_identity_evidence(self):
        self.contract['endpoint_control']['identity_sources'].pop()
        self.save()
        with self.assertRaisesRegex(SystemExit,'身份来源集合'):
            validate_endpoint_characters(self.md,'',self.prompt,self.refs)

    def test_frame_mode_cannot_bypass_native_dialogue_voice_binding(self):
        with self.assertRaisesRegex(SystemExit,'声音参考绑定'):
            validate_endpoint_characters(self.md,'类型: 正常台词',self.prompt,self.refs)


if __name__ == '__main__':
    unittest.main()
