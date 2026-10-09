import unittest,copy
from unittest.mock import patch
from support import fixture,PROBE,load
from core import release_errors,fingerprint,local

class ReleaseGateTests(unittest.TestCase):
    def setUp(self):self.temp,self.root,self.db=fixture()
    def tearDown(self):self.temp.cleanup()
    def errors(self):
        with patch('core.probe',return_value=PROBE):return release_errors(self.db,self.root)
    def test_complete_synthetic_fixture_passes(self):self.assertEqual(self.errors(),[])
    def test_current_film_blocked(self):self.assertTrue(release_errors(load()))
    def test_uncleared_asset_blocks(self):
        for status in ['unknown','permission_requested','legal_review_required','rejected']:
            self.db['rights'][0]['status']=status;self.assertTrue(self.errors())
    def test_pending_human_approval_blocks(self):self.db['approvals']['publication_approved']=False;self.assertTrue(self.errors())
    def test_placeholder_blocks_even_if_paper_approved(self):
        self.db['timeline']['cuts']['master']['segments'][0]['kind']='placeholder';self.db['approvals']['input_sha256']=fingerprint(self.db,self.root)['input_sha256'];self.assertTrue(self.errors())
    def test_changed_media_invalidates_approval(self):
        (self.root/'test.bin').write_bytes(b'changed');self.assertTrue(self.errors())
    def test_changed_renderer_invalidates_approval(self):
        (self.root/'scripts/render.py').write_text('changed');self.assertTrue(self.errors())
    def test_changed_evidence_invalidates_approval(self):
        (self.root/'evidence.txt').write_text('changed');self.assertTrue(self.errors())
    def test_path_traversal_blocked(self):
        with self.assertRaises(ValueError):local(self.root,'../outside.txt')
    def test_caption_transcript_mismatch(self):
        self.db['clips'][0]['caption_cues'][0]['text']='different';self.assertTrue(self.errors())
    def test_declared_resolution_mismatch(self):
        self.db['sources'][0]['width']=999;self.assertTrue(self.errors())
    def test_actual_media_bounds(self):
        with patch('core.probe',return_value={**PROBE,'format':{'duration':'.5'}}):self.assertTrue(release_errors(self.db,self.root))
    def test_public_domain_label_alone_insufficient(self):
        self.db['rights'][0].update(status='public_domain_verified',evidence_path=None);self.assertTrue(self.errors())
    def test_final_render_calls_gate_before_creating_files(self):
        from render import render_cut
        with self.assertRaises(ValueError):render_cut(load(),'master',self.root/'should-not-exist','final')
        self.assertFalse((self.root/'should-not-exist').exists())
