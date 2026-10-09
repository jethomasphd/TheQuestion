"""Purpose-composed 90-second and 60-second review edits; no archive recropping."""
from director_cut import *

def derivative(kind,out):
 script=json.loads((R/'data/director_narration.json').read_text(encoding='utf8'))
 base=plan(script);by_name={s.get('narration'):s for s in base if s['kind']=='narration'}
 if kind=='trailer':
  scenes=[dict(by_name['opening']),dict(kind='card',duration=5,title='THE QUESTION\nTHAT REMAINS',subtitle='An invitation to examine a life',bg='threshold'),dict(by_name['knowledge_out']),dict(by_name['ending']),dict(kind='card',duration=0,title='“But who do you say\nthat I am?”',subtitle='Mark 8:29a · World English Bible Classic',bg='black'),dict(kind='card',duration=4,title='THE QUESTION REMAINS.',subtitle='',bg='black')]
  scenes[-2]['duration']=90-sum(s['duration'] for s in scenes);w,h=1920,1080;name='trailer_90s'
 else:
  scenes=[dict(by_name['opening']),dict(kind='card',duration=3,title='THE QUESTION\nTHAT REMAINS',subtitle='',bg='water'),dict(by_name['ending']),dict(kind='card',duration=0,title='“But who do you\nsay that I am?”',subtitle='Mark 8:29a\nWorld English Bible Classic',bg='black')]
  scenes[-1]['duration']=60-sum(s['duration'] for s in scenes);w,h=1080,1920;name='vertical_60s'
 t=0
 for i,s in enumerate(scenes):s.update(start=t,id=f'{kind}_{i:02}');t+=s['duration']
 paths=[]
 for s in scenes:
  p=W/(s['id']+'.mkv');render_scene(s,p,w,h);paths.append(p)
 joined=W/(name+'_joined.mkv');concat(paths,joined);dest=out/(name+'.mp4');make_captions(scenes,dest);mix(scenes,joined,dest)
 write(out/(name+'_timeline.json'),scenes);print('DERIVATIVE FINISHED',dest,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--cut',choices=['trailer','vertical'],required=True);a=p.parse_args();derivative(a.cut,a.output)
