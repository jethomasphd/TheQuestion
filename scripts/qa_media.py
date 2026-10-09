"""Decode and inspect media timing, stream layout, black frames and audio level."""
import argparse,re,json
from core import probe,binary,run,write_json
import subprocess

def inspect(path,expected=None):
    data=probe(path);video=next(s for s in data['streams'] if s['codec_type']=='video');audio=next((s for s in data['streams'] if s['codec_type']=='audio'),None)
    duration=float(data['format']['duration']);errors=[]
    if expected is not None and abs(duration-expected)>.08:errors.append('Duration mismatch')
    if not audio:errors.append('Missing audio stream')
    if audio and abs(float(video.get('duration',duration))-float(audio.get('duration',duration)))>.08:errors.append('Audio/video duration differs')
    p=subprocess.run([binary('ffmpeg'),'-hide_banner','-i',str(path),'-vf','blackdetect=d=1:pix_th=0.04:pic_th=0.999','-af','volumedetect','-f','null','-'],capture_output=True,text=True,encoding='utf-8',errors='replace')
    if p.returncode:errors.append('Full decode failed')
    black=re.findall(r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)',p.stderr)
    peak=re.search(r'max_volume: ([\-\w.]+) dB',p.stderr)
    if peak and peak.group(1)!='-inf' and float(peak.group(1))>-1:errors.append('Sample peak exceeds -1 dBFS; true-peak assessment also required')
    result={'path':str(path),'duration_seconds':duration,'width':video['width'],'height':video['height'],'frame_rate':video['r_frame_rate'],'audio_channels':audio.get('channels') if audio else None,'black_intervals':black,'sample_peak_dbfs':peak.group(1) if peak else None,'errors':errors,'note':'Black/silence holds and fade boundaries must be compared to the timeline. This does not replace human viewing/listening or final EBU R128 true-peak measurement.'}
    write_json(str(path)+'.qa.json',result);return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path');p.add_argument('--duration',type=float);a=p.parse_args();r=inspect(a.path,a.duration);print(json.dumps(r,indent=2));raise SystemExit(bool(r['errors']))
