import json,sys,unittest,uuid,shutil
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import director_cut as cut

class DirectorCutTests(unittest.TestCase):
 def test_plan_is_contiguous_and_frame_aligned(self):
  script=json.loads((cut.R/'data/director_narration.json').read_text(encoding='utf8'))
  with patch.object(cut,'dur',return_value=18):scenes=cut.plan(script)
  end=0
  for s in scenes:
   self.assertAlmostEqual(s['start'],end,places=5)
   self.assertAlmostEqual(s['duration']*24,round(s['duration']*24),places=5)
   end+=s['duration']
  self.assertGreaterEqual(end,420);self.assertLessEqual(end,540)
  self.assertEqual([s['excerpt'] for s in scenes if s['kind']=='archive'],list(cut.EXCERPTS))

 def test_caption_source_offset_and_playback_speed(self):
  root=cut.R/'work/test-fixtures'/str(uuid.uuid4());folder=root/'work/transcripts';folder.mkdir(parents=True)
  try:
   data=[{'start':0,'end':5,'text':'ignored','words':[{'start':1,'end':2,'word':'Outside.'},{'start':3,'end':4,'word':'Inside.'}]}]
   for name in ['example','narr_example']:(folder/(name+'.json')).write_text(json.dumps(data),encoding='utf8')
   with patch.object(cut,'R',root),patch.object(cut,'SPEED',.5):
    cut.make_captions([{'kind':'archive','source':'example','excerpt':'example','source_in':2.5,'source_out':4.5,'start':10,'duration':2}],root/'clip')
    self.assertEqual(json.loads((root/'clip.json').read_text())[0],[10.5,11.5,'Inside.'])
    cut.make_captions([{'kind':'narration','narration':'example','start':20,'duration':12}],root/'narr')
    self.assertAlmostEqual(json.loads((root/'narr.json').read_text())[0][0],22.9)
   self.assertTrue((root/'clip.vtt').read_text().startswith('WEBVTT'))
  finally:
   self.assertTrue(root.resolve().is_relative_to((cut.R/'work/test-fixtures').resolve()));shutil.rmtree(root)

 def test_production_approval_does_not_reclassify_copyright(self):
  for name in ['king','collins','fry','bono','curry','carrey']:self.assertEqual(cut.SPEAKERS[name]['rights'],'legal_review_required')
  self.assertEqual(cut.SPEAKERS['obama']['rights'],'public_domain_verified')

 def test_speech_normalization_keeps_contiguous_audio_packets(self):
  if not Path(cut.F).exists() and not shutil.which(cut.F):self.skipTest('FFmpeg unavailable')
  root=cut.R/'work/test-fixtures'/str(uuid.uuid4());root.mkdir(parents=True)
  try:
   source=root/'tone.wav';out=root/'normalized.mkv'
   cut.ff('-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=4','-c:a','pcm_s16le',source)
   af=cut.speech_filter(source,0,6,'narration')
   cut.ff('-i',source,'-af',af,'-c:a','pcm_s16le','-ar','48000',out)
   packets=json.loads(cut.run([cut.P,'-v','error','-select_streams','a','-show_packets','-show_entries','packet=pts_time,duration_time','-of','json',out]))['packets']
   end=0
   for pkt in packets:
    start=float(pkt['pts_time']);self.assertLess(abs(start-end),.002)
    end=start+float(pkt['duration_time'])
   self.assertAlmostEqual(end,6,places=2)
  finally:
   self.assertTrue(root.resolve().is_relative_to((cut.R/'work/test-fixtures').resolve()));shutil.rmtree(root)

if __name__=='__main__':unittest.main()
