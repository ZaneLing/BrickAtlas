"""Check the exported Markdown against assets, public handles and saved GT.

The generator already replays native executors. This checks the actual document,
not another implementation of the assembly rules. It also makes a local preview.
"""
from pathlib import Path
from collections import Counter
from hashlib import sha256
from html import escape
import json
import re
from urllib.parse import unquote,urlparse
import numpy as np
from PIL import Image
from markdown_it import MarkdownIt

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'deliverables/brickplan-question-showcase'


def read(p):return json.loads(p.read_text())


def main():
    manifest=read(OUT/'manifest.json');selection=read(OUT/'selection.json')
    examples=[read(p) for p in sorted((OUT/'examples').glob('Q*.json'))]
    assert len(examples)==manifest['examplesCount']
    assert len({(r['bank'],r['mode'],r['family'],r['level']) for r in selection if r['purpose']=='coverage'})==manifest['completeCellCoverage']
    assert not any('cascade' in r['family'] for r in examples)
    assert len({r['model'] for r in examples if r['bank']=='E7'})==21
    for source,expected in manifest['sourceFiles'].items():assert sha256((ROOT/source).read_bytes()).hexdigest()==expected,source
    asset_records={};action_count=0
    forbidden={'privateEvent','oraclePlan','referenceActions','humanErrorIds','goal','initial','family','intervention','eventApplied'}
    def clean(value):
        if isinstance(value,dict):
            assert not forbidden.intersection(value),(forbidden.intersection(value))
            for v in value.values():clean(v)
        elif isinstance(value,list):
            for v in value:clean(v)
    def collect(value):
        if isinstance(value,dict):
            if all(k in value for k in ('file','sha256','width','height')):asset_records[value['file']]=value
            for v in value.values():collect(v)
        elif isinstance(value,list):
            for v in value:collect(v)
    for e in examples:
        collect(e);gt=read(OUT/e['gtFile']);assert gt['referenceWitnessPassed'] and not gt['humanOrModelPerformance']
        assert len(gt['referenceActions'])==e['referenceActions']
        action_count+=e['referenceActions']
        packets=[e['initial'],*[event['packet'] for event in e['events']]]
        initial=read(OUT/e['initial']['input'])['observation']
        handles=initial.get('handles',initial.get('actionHandles'))
        allowed={h.get('partId',h.get('id')):set(h['candidates']) for h in handles}
        for a in gt['referenceActions']:
            p=a['publicAction'];assert p['partId'] in allowed
            if p['type']=='attach':assert p['candidate'] in allowed[p['partId']]
            assert a['feedback']=='OK'
        for packet in packets:
            data=read(OUT/packet['input']);clean(data['observation'])
            assert len([r for r in data['images'] if r['role']=='current-target'])==3
            if packet is e['initial']:assert not any(r['role']=='temporal-pair' for r in data['images'])
            else:assert len([r for r in data['images'] if r['role']=='temporal-pair'])==3
        image=np.asarray(Image.open(OUT/e['finalImage']['file']).convert('RGB'))
        assert np.array_equal(image[36:636,:800],image[36:636,800:1600]),e['example']
    for path,record in asset_records.items():
        data=(OUT/path).read_bytes();assert sha256(data).hexdigest()==record['sha256'],path
        with Image.open(OUT/path) as im:assert im.size==(record['width'],record['height']),path
    markdown=(OUT/'README.zh-CN.md').read_text()
    md=MarkdownIt('commonmark',{'html':True}).enable('table');tokens=md.parse(markdown)
    links=[];images=[]
    for token in tokens:
        for child in token.children or []:
            if child.type=='image':
                src=child.attrGet('src');images.append(src)
                with Image.open(OUT/src) as im:w,h=im.size
                child.attrSet('width',str(w));child.attrSet('height',str(h));child.attrSet('loading','lazy')
            if child.type=='link_open':links.append(child.attrGet('href'))
    for path in images+links:
        if path.startswith('#'):
            if path[1:].startswith('q'):assert f'id="{path[1:]}"' in markdown,path
            continue
        if urlparse(path).scheme:continue
        assert (OUT/unquote(path.split('#')[0])).is_file(),path
    # Give headings predictable anchors in the plain HTML preview.
    for i,token in enumerate(tokens):
        if token.type=='heading_open':
            title=tokens[i+1].content.lower()
            token.attrSet('id',re.sub(r'[^\w\-\s\u4e00-\u9fff]','',title).replace(' ','-'))
    html=md.renderer.render(tokens,md.options,{})
    style='''*{box-sizing:border-box}body{margin:0;background:#f2f5f9;color:#183047;font:16px/1.75 system-ui,-apple-system,sans-serif}main{max-width:1440px;margin:auto;background:white;padding:32px}h1{font-size:30px}h2{margin-top:48px;padding-top:18px;border-top:2px solid #d9e4ee}h3{margin-top:45px;padding:12px;background:#eef5fd;border-left:5px solid #2768ac}table{border-collapse:collapse;width:100%;margin:16px 0 24px;table-layout:fixed}th,td{border:1px solid #dce4ec;padding:8px;vertical-align:top;overflow-wrap:anywhere}th{background:#f2f6fa}img{max-width:100%;height:auto;cursor:zoom-in}pre{background:#f0f3f8;padding:14px;overflow:auto}code{font-size:13px;overflow-wrap:anywhere}a{color:#1966ac}blockquote{margin:16px 0;padding:12px;background:#fff4da}.notice{background:#fff1d8;padding:14px;border-radius:8px}nav{position:sticky;top:0;background:#f5f8fcf5;padding:12px;z-index:3}nav a{margin-right:20px}dialog{max-width:96vw;max-height:94vh;padding:12px;border:0;box-shadow:0 0 0 100vmax #0009;overflow:auto}dialog img{max-width:none;width:auto}dialog button{position:sticky;left:0;top:0;display:block;z-index:5;font:inherit;margin-bottom:8px;padding:6px 14px;cursor:pointer}dialog a{display:block}p{overflow-wrap:anywhere}@media(max-width:650px){main{padding:14px}table{display:block;overflow:auto}th,td{min-width:130px}}'''
    style+='[id]{scroll-margin-top:70px}'
    preview='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>题目图解：输入、输出与GT</title><style>'''+style+'''</style><main><nav><a href="#按类别和难度找题">分类索引</a><a href="#难度怎么读">难度说明</a><a href="README.zh-CN.md">Markdown原文件</a></nav><p class="notice">这是同一份Markdown的本机预览，包含GT供审题。图片按需加载；点击图片按原始分辨率查看，关闭后继续阅读。</p>'''+html+'''</main><dialog id="zoom"><button>关闭</button><a target="_blank">单独打开原图</a><img alt="原始分辨率图像"></dialog><script>const d=document.querySelector('#zoom');for(const im of document.querySelectorAll('main img')){im.loading='lazy';im.onclick=()=>{d.querySelector('img').src=im.src;d.querySelector('a').href=im.src;d.showModal();}}d.querySelector('button').onclick=()=>d.close();</script></html>'''
    (OUT/'preview.html').write_text(preview)
    report=dict(status='PASS',examples=len(examples),populatedCategoryModeLevelCells=manifest['completeCellCoverage'],newConfigurationsCovered=21,
        nativeReferenceWitnessesPassed=manifest['referenceWitnessesPassed'],nativeAcceptedManipulations=action_count,
        imagesEmbeddedInMarkdown=len(images),uniqueImagesLinked=len(set(images)),allLocalLinksExist=True,
        assetFilesHashed=len(asset_records),allGTFinalScenePixelsMatchTarget=True,
        publicActionHandlesAndCandidatesMatch=True,publicObservationsContainNoGT=True,
        firstObservationHasNoTemporalPair=True,eventObservationsHaveThreeTemporalViews=True,
        checkerSha256=sha256(Path(__file__).read_bytes()).hexdigest(),apiModelCalls=0,
        humanReadabilityAndEmpiricalDifficulty='pending')
    (OUT/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))


if __name__=='__main__':main()
