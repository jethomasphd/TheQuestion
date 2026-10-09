from core import ROOT,load,assert_valid,local,binary,run,sha,write_json

def main():
    db=load();assert_valid(db);out=ROOT/'assets/proxy';out.mkdir(parents=True,exist_ok=True);done={}
    for c in db['clips']:
        if not c['media_path']:continue
        source=local(ROOT,c['media_path']);local(ROOT,c['acquisition_evidence_path'])
        if sha(source)!=c['source_sha256']:raise ValueError('Source checksum mismatch')
        if c['source_id'] in done:continue
        dest=out/(c['source_id']+'.mp4')
        run([binary('ffmpeg'),'-hide_banner','-loglevel','error','-y','-i',source,'-vf','scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1','-c:v','libx264','-preset','fast','-crf','23','-c:a','aac',dest])
        done[c['source_id']]={'source_sha256':sha(source),'proxy_sha256':sha(dest)}
    write_json(ROOT/'outputs/reports/proxies.json',done);print(f'{len(done)} authorized local sources processed')

if __name__=='__main__':main()
