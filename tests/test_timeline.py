import unittest
from support import load
from core import validate,fingerprint

class TimelineTests(unittest.TestCase):
    def test_exact_delivery_durations(self):
        d=load()['timeline']['cuts'];self.assertEqual([d[k]['duration_ms'] for k in ['master','trailer','vertical']],[495000,90000,60000])
    def test_gap_and_overlap_rejected(self):
        for shift in [-1000,1000]:
            d=load();d['timeline']['cuts']['master']['segments'][1]['start_ms']+=shift;self.assertTrue(validate(d))
    def test_source_bounds(self):
        d=load();d['sources'][0]['duration_ms']=500;d['clips'][0].update(source_in_ms=0,source_out_ms=1000);self.assertTrue(validate(d))
    def test_reproducible_fingerprint(self):self.assertEqual(fingerprint(load()),fingerprint(load()))
    def test_quote_cannot_hide_asset(self):
        d=load();s=next(s for s in d['timeline']['cuts']['master']['segments'] if s['kind']=='quote');s['asset_ids'].remove('SCRIPTURE_WEB');self.assertTrue(validate(d))
    def test_font_asset_cannot_be_omitted(self):
        d=load();d['timeline']['cuts']['master']['segments'][0]['asset_ids'].remove('FONTS');self.assertTrue(validate(d))
