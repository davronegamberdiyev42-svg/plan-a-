#!/usr/bin/env python3
"""Static/data/media QA for IELTS Boost Plan A. Does not replace device E2E."""
from pathlib import Path
from bs4 import BeautifulSoup
import json, hashlib, re, subprocess, sys, collections, os
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def add(name, ok, detail=''):
    checks.append({'name':name,'pass':bool(ok),'detail':str(detail)[:500]})
def load_json(p):
    return json.loads(p.read_text(encoding='utf-8'))
def node_check(src,name):
    tmp=Path('/tmp')/f'pa_{name.replace("/","_")}.js'
    tmp.write_text(src,encoding='utf-8')
    r=subprocess.run(['node','--check',str(tmp)],capture_output=True,text=True)
    return r.returncode==0,(r.stderr.strip() or 'node --check PASS')

index=ROOT/'index.html'; standalone=ROOT/'standalone.html'
soup=BeautifulSoup(index.read_text(encoding='utf-8',errors='replace'),'html.parser')
app_tag=soup.find('script',id='appData')
try:
    app=json.loads(app_tag.string or app_tag.text)
    app_ok=True
except Exception as e:
    app={}; app_ok=False; app_err=str(e)
add('main_app_data_json',app_ok,'embedded appData parsed' if app_ok else app_err)
plan=app.get('plan',{}).get('days',[]); core=app.get('core',{}).get('days',[])
add('plan_84_days',len(plan)==84,len(plan))
add('core_84_days',len(core)==84,len(core))
add('4_skill_modules_each_day',len(core)==84 and all(set(['reading','listening','writing','speaking']).issubset(x.keys()) for x in core), '84 days × 4 core skills')
reading_q=sum(len(x.get('reading',{}).get('questions',[])) for x in core)
listening_q=sum(len(x.get('listening',{}).get('questions',[])) for x in core)
add('reading_question_count',reading_q==840,reading_q)
add('listening_question_count',listening_q==420,listening_q)
sp_days=app.get('speakingExpert',{}).get('days',[])
part1=sum(len(x.get('part1',[])) for x in sp_days); part2=sum(1 for x in sp_days if x.get('part2')); part3=sum(len(x.get('part3',[])) for x in sp_days)
add('speaking_prompts',len(sp_days)==84 and part1==252 and part2==84 and part3==252, f'P1={part1}; P2={part2}; P3={part3}')
add('writing_prompts',all(x.get('writing',{}).get('task1_prompt') and x.get('writing',{}).get('task2_prompt') for x in core), 'Task 1 + Task 2 prompts all days')
add('articles_61',len(app.get('library',{}).get('articles',[]))==61,len(app.get('library',{}).get('articles',[])))
add('sentence_patterns_864',len(app.get('patterns',[]))==864,len(app.get('patterns',[])))
add('reading_packs_12',len(app.get('readingSourcePacks',[]))==12,len(app.get('readingSourcePacks',[])))
words=app.get('words',[])
terms=[re.sub(r'\s+',' ',str(x.get('word','')).strip().casefold()) for x in words]
add('vocabulary_19k',len(words)==19000,len(words))
add('vocabulary_unique_terms',len(set(terms))==19000,len(set(terms)))
daily=app.get('vocabularyExpert',{}).get('daily_sets',[])
ids=[i for row in daily for i in row.get('word_ids',[])]
lookup={x.get('id'):x for x in words}
add('daily_sets_84x8',len(daily)==84 and all(len(x.get('word_ids',[]))==8 for x in daily), f'{len(daily)} sets / {len(ids)} ids')
add('daily_core_672_unique',len(ids)==672 and len(set(ids))==672 and all(i in lookup for i in ids),f'{len(ids)} ids, {len(set(ids))} unique, unresolved={sum(i not in lookup for i in ids)}')
add('daily_core_dual_ipa',all(lookup[i].get('ipa_us') and lookup[i].get('ipa_uk') for i in ids), 'US + UK IPA present for every daily core entry')
add('daily_core_full_gloss',all(lookup[i].get('meaning_en') and lookup[i].get('uzbek') and lookup[i].get('example') and lookup[i].get('part_of_speech') for i in ids), 'definition, Uzbek gloss, example and POS on 672 core')

# Stage 47/48 linked data packs
skills=load_json(ROOT/'data/stage47-skill-resources.json')
listening=load_json(ROOT/'data/stage47-listening-companions.json')
task1=load_json(ROOT/'data/stage47-task1-datasets.json')
coverage=load_json(ROOT/'data/stage48-vocabulary-coverage.json')
add('stage47_skill_resources_336',len(skills)==336,len(skills))
byday=collections.defaultdict(list)
for row in skills: byday[int(row['day'])].append(str(row['skill']).casefold())
add('stage47_4_skills_each_day',len(byday)==84 and all(len(v)==4 and len(set(v))==4 for v in byday.values()),'84 × 4 unique skill names')
add('stage47_listening_companions_84',len(listening)==84,len(listening))
add('stage47_task1_datasets_84',len(task1)==84,len(task1))
fams=collections.Counter(x.get('visual_type') for x in task1)
add('task1_six_families_14_each',len(fams)==6 and all(v==14 for v in fams.values()),dict(fams))
# Ensure every day has a dataset, and data has an explicit fictional provenance.
add('task1_day_coverage',set(int(x['day']) for x in task1)==set(range(1,85)),'days 1..84 exactly')
add('task1_provenance_disclosed',all('fictional' in str(x.get('provenance','')).casefold() or 'illustrative' in str(x.get('provenance','')).casefold() for x in task1),'fictional practice datasets labelled')
add('daily_core_coverage_record',coverage.get('total_indexed')==19000 and coverage.get('daily_core',{}).get('items')==672,coverage.get('daily_core'))
# Data-structure readability sanity checks.
parsed=0; malformed=[]
for row in task1:
    typ=row['visual_type']; raw=row.get('data_structure','')
    if typ=='process': ok='→' in raw
    elif typ=='map': ok='→' in raw and ';' in raw
    else: ok=bool(re.search(r'-?\d+(?:\.\d+)?',raw)) and ':' in raw
    parsed+=bool(ok)
    if not ok: malformed.append(row['day'])
add('task1_data_structures_parse',parsed==84,f'{parsed}/84; malformed={malformed[:10]}')

# MP3 presence and actual decode.
audio=sorted((ROOT/'audio').glob('listening-day-*.mp3'))
add('audio_84_assets',len(audio)==84,sum(p.stat().st_size for p in audio))
missing=[f'{i:02d}' for i in range(1,85) if not (ROOT/'audio'/f'listening-day-{i:02d}.mp3').exists()]
add('audio_day_sequence',not missing,'missing days '+','.join(missing))
decode_ok=0; decode_fail=[]
for p in audio:
    r=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True,text=True)
    if r.returncode==0 and not r.stderr.strip(): decode_ok+=1
    else: decode_fail.append((p.name,r.stderr.strip()[:160]))
add('ffmpeg_audio_decode_84',decode_ok==84,f'{decode_ok}/84; failures={decode_fail[:3]}')

# HTML, JS, CSS and PWA paths.
css=ROOT/'assets/css/stage40-50.css'; js=ROOT/'assets/js/stage40-50.js'; sw=ROOT/'sw.js'
add('module_css_js_present',css.exists() and js.exists(),f'css={css.stat().st_size if css.exists() else 0}; js={js.stat().st_size if js.exists() else 0}')
for name,p in [('stage4050_js',js),('service_worker',sw)]:
    ok,detail=node_check(p.read_text(encoding='utf-8'),name)
    add(name+'_syntax',ok,detail)
# Check executable inline JS (exclude appData and embedded module JSON).
inline=[]
for i,tag in enumerate(soup.find_all('script')):
    if tag.get('src') or tag.get('type') in ('application/json','application/ld+json'): continue
    txt=tag.string or tag.text or ''
    if txt.strip(): inline.append((i,txt))
inline_results=[]
for i,txt in inline:
    ok,detail=node_check(txt,f'inline_{i}')
    inline_results.append((i,ok,detail))
add('main_inline_js_syntax',all(x[1] for x in inline_results),inline_results)
manifest=load_json(ROOT/'manifest.webmanifest')
add('pwa_manifest_relative_scope',manifest.get('scope')=='./' and manifest.get('start_url','').startswith('./'),manifest.get('scope'))
add('pwa_manifest_icons',len(manifest.get('icons',[]))>=2,[x.get('src') for x in manifest.get('icons',[])])
required=['./manifest.webmanifest','./favicon.svg','./assets/css/stage40-50.css','./assets/js/stage40-50.js','./data/stage47-skill-resources.json','./data/stage47-listening-companions.json','./data/stage47-task1-datasets.json','./data/stage48-vocabulary-coverage.json','./icons/icon-192.png','./icons/icon-512.png','./sw.js']
missing=[]
for ref in required:
    if not (ROOT/ref[2:]).exists(): missing.append(ref)
add('all_runtime_assets_exist',not missing,missing or f'{len(required)} required assets exist')
add('no_old_repo_absolute_paths','/Ielts-gooo/' not in index.read_text(encoding='utf-8',errors='ignore'), 'No hard-coded old repo base path')
# Required Stage 40-50 feature hooks in extension.
feature_src=js.read_text(encoding='utf-8')
features=['openAudioDB','MediaRecorder','audioClipsMarkup','calculateScore','adaptiveRecommendations','resourcesView','task1View','vocabularyView','privacyView','releaseView','backupExport','clearAudioDB','release-recheck']
missing_features=[x for x in features if x not in feature_src]
add('stage4050_feature_hooks',not missing_features,missing_features or f'{len(features)} named feature hooks')
add('resource_skill_filter_case_insensitive',"norm(r.skill)===norm(skill)" in feature_src,'case-normalized skill filter')
add('dialog_focus_management','lastFocusedElement' in feature_src and "e.key==='Tab'" in feature_src,'focus restoration and Tab trap')
add('reduced_motion_and_focus_css','prefers-reduced-motion:reduce' in css.read_text() and ':focus-visible' in css.read_text(),'reduced motion and keyboard focus states')

# Standalone companion embeds data, CSS and module JS.
stand=BeautifulSoup(standalone.read_text(encoding='utf-8',errors='replace'),'html.parser')
stand_data=stand.find('script',id='ib4050-embedded-data')
stand_js=stand.find('script',id='stage40-50-inline-js')
stand_css=stand.find('style',id='stage40-50-inline-css')
try:
    pack=json.loads(stand_data.string or stand_data.text)
    data_embedded=(len(pack.get('skills',[]))==336 and len(pack.get('listening',[]))==84 and len(pack.get('task1',[]))==84)
except Exception as e:
    data_embedded=False; pack_err=str(e)
add('standalone_embedded_data',data_embedded,'336 skills + 84 listening + 84 Task1')
add('standalone_inline_css_js',bool(stand_css and stand_js) and len(stand_js.string or stand_js.text)>60000 and len(stand_css.string or stand_css.text)>12000,'embedded Final Studio CSS + JS')
if stand_js:
    ok,detail=node_check(stand_js.string or stand_js.text,'standalone_stage4050')
else: ok,detail=False,'missing inline module'
add('standalone_module_js_syntax',ok,detail)
# Standalone is intended to be used with audio/ folder for MP3 playback, not as a fully self-contained media archive.
add('standalone_title_present',bool(stand.title and 'Plan A' in stand.title.text),stand.title.text if stand.title else 'missing title')

# Stage map/limitations and target instructions must be explicit.
readme=(ROOT/'README_UZ.md').read_text(encoding='utf-8')
add('plan_a_deploy_instructions','plan-a-' in readme and 'main' in readme and 'root' in readme,'repo root upload guidance')
add('limitations_disclosed',('Stage 40 original ZIP' in readme or 'Stage 40 original' in readme or 'original Stage 40' in readme) and 'kafolatlamaydi' in readme,'source/score limitations disclosure')

passed=sum(x['pass'] for x in checks); total=len(checks)
report={'release':'50.2.0-plan-a','passed':passed,'total':total,'failures':[x for x in checks if not x['pass']],'checks':checks,'limitations':['Browser UI automation is blocked in this environment (ERR_BLOCKED_BY_ADMINISTRATOR); no UI end-to-end PASS is claimed.','Real Android microphone / ASR / PWA install and production hosted offline behavior require a physical-device test.','Exact original Stage 40 source archive and all historical 41–50 patch commits are not available; final is an enhanced reconstruction from preserved baseline and records.','IELTS practice score is not an official IELTS band; 8–9 is not guaranteed.']}
(ROOT/'docs').mkdir(exist_ok=True)
(ROOT/'docs'/'STATIC_QA_50_2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(0 if passed==total else 2)
