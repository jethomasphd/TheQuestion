import unittest
from support import load
from captions import validate_cues,cues_for

class CaptionTests(unittest.TestCase):
    def test_all_cut_caption_timings(self):
        d=load()
        for cut in d['timeline']['cuts'].values():self.assertFalse(validate_cues(cues_for(cut,d),cut['duration_ms']))
    def test_overlap(self):self.assertTrue(validate_cues([dict(start_ms=0,end_ms=80,text='a'),dict(start_ms=70,end_ms=90,text='b')],100))
    def test_out_of_bounds(self):self.assertTrue(validate_cues([dict(start_ms=0,end_ms=110,text='a')],100))
    def test_missing_speech_is_labeled(self):
        d=load();cues=cues_for(d['timeline']['cuts']['master'],d);self.assertTrue(any('no recorded speech' in c['text'] for c in cues))
