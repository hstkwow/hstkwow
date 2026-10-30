#!/usr/bin/env python3
"""Generate self-hosted SVG animations from GitHub's contribution calendar."""
from pathlib import Path
import argparse,html,json,os,urllib.request,datetime,math
ROOT=Path(__file__).resolve().parents[1]
PALETTES={'dark':dict(bg='#0d1117',ink='#e6edf3',muted='#9da7b3',line='#30363d',accent='#f59e87',cells=['#161b22','#4a302c','#784b3f','#b8755b','#f59e87']), 'light':dict(bg='#ffffff',ink='#24292f',muted='#57606a',line='#d0d7de',accent='#ad4834',cells=['#ebedf0','#f3d8c7','#dda88e','#c97555','#ad4834'])}
def svg(w,h,content,label):return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(label,quote=True)}"><title>{html.escape(label)}</title>{content}</svg>'''
def banner(p):
 positions=';'.join(f'{112*math.cos(i*math.tau/72):.3f} {42*math.sin(i*math.tau/72):.3f}' for i in range(73))
 angles=[]
 for i in range(73):
  a=math.degrees(math.atan2(42*math.cos(i*math.tau/72),-112*math.sin(i*math.tau/72)))
  while angles and a<angles[-1]:a+=360
  angles.append(a)
 turns=';'.join(f'{a:.3f}' for a in angles)
 content=f'''<defs><clipPath id="typing"><rect width="470" height="30"><animate attributeName="width" values="0;470;470;0;0" keyTimes="0;.25;.75;.9;1" dur="10s" repeatCount="indefinite"/></rect></clipPath><path id="orbit" d="M 74 0 A 112 42 0 1 1 -74 0 A 112 42 0 1 1 74 0"/></defs>
<rect x=".5" y=".5" width="979" height="239" rx="14" fill="{p['bg']}" stroke="{p['line']}"/>
<g font-family="Arial,Helvetica,sans-serif"><text x="36" y="40" fill="{p['accent']}" font-size="11" letter-spacing="2">HSTK / RESEARCH &amp; ENGINEERING</text><text x="34" y="103" fill="{p['ink']}" font-size="47" font-weight="700">Sun Tao.</text><text x="36" y="137" fill="{p['muted']}" font-size="16">Graduate student · Tiangong University</text>
<g transform="translate(36 162)" clip-path="url(#typing)" fill="{p['accent']}" font-size="17"><text y="21" opacity="1">Pansharpening. A sharper view of Earth.<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.45;.5;1" dur="20s" repeatCount="indefinite"/></text><text y="21" opacity="0">From algorithms to working systems.<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;.45;.5;1" dur="20s" repeatCount="indefinite"/></text></g><text x="36" y="218" fill="{p['muted']}" font-size="10" letter-spacing="1.8">OBSERVE · UNDERSTAND · BUILD</text></g>
<g transform="translate(774 123)"><circle r="66" fill="none" stroke="{p['line']}" stroke-width="1.3"/><g fill="none" stroke="{p['line']}"><ellipse rx="24" ry="66"/><ellipse rx="49" ry="66"/><ellipse rx="66" ry="23"/><ellipse rx="66" ry="48"/><path d="M-66 0H66M0-66V66"/></g><g transform="rotate(-25)"><ellipse rx="112" ry="42" fill="none" stroke="{p['accent']}" stroke-dasharray="4 5" opacity=".65"/><g transform="translate(112 0)"><animateTransform attributeName="transform" type="translate" values="{positions}" dur="18s" repeatCount="indefinite"/><g transform="rotate(90)"><animateTransform attributeName="transform" type="rotate" values="{turns}" dur="18s" repeatCount="indefinite"/><g fill="{p['bg']}" stroke="{p['accent']}" stroke-width="1.4"><rect x="-6" y="-7" width="12" height="14"/><path d="M-20-8H-10V8H-20ZM10-8H20V8H10ZM-15-8V8M15-8V8M0-7V-14"/></g></g></g></g></g>'''
 # Use exactly the same centered ellipse for the satellite motion and the visible orbit.
 content=content.replace('M 74 0 A 112 42 0 1 1 -74 0 A 112 42 0 1 1 74 0','M 112 0 A 112 42 0 1 1 -112 0 A 112 42 0 1 1 112 0')
 return svg(980,240,content,'Sun Tao / HSTK. Remote sensing, pansharpening, and engineering. Animated satellite orbit and research title.')
def calendar(data,p):
 weeks=data['weeks'];step=15;grid_width=len(weeks)*step;w=980
 rects=[];labels=[];last_month=None
 for x,week in enumerate(weeks):
  for day in week['contributionDays']:
   date=datetime.date.fromisoformat(day['date']);y=(date.weekday()+1)%7;count=day['contributionCount'];level=0 if not count else 1 if count<3 else 2 if count<6 else 3 if count<10 else 4
   rects.append(f'<rect x="{x*step}" y="{y*step}" width="11" height="11" rx="2" fill="{p["cells"][level]}"><title>{date}: {count} contributions</title></rect>')
   month=date.strftime('%b')
   if month!=last_month and (last_month is None or date.day==1):
    if not labels or x*step-int(labels[-1][0])>30:labels.append((x*step,month))
    last_month=month
 month_svg=''.join(f'<text x="{x}" y="-10">{month}</text>' for x,month in labels)
 total=data['totalContributions'];first=weeks[0]['contributionDays'][0]['date'];last=weeks[-1]['contributionDays'][-1]['date']
 content=f'''<defs><clipPath id="grid"><rect width="{grid_width}" height="105"/></clipPath><linearGradient id="beam"><stop stop-color="{p['accent']}" stop-opacity="0"/><stop offset="1" stop-color="{p['accent']}" stop-opacity=".22"/></linearGradient></defs><rect x=".5" y=".5" width="979" height="235" rx="14" fill="{p['bg']}" stroke="{p['line']}"/>
<g font-family="Arial,Helvetica,sans-serif"><text x="32" y="32" font-size="11" letter-spacing="2" fill="{p['accent']}">THE ACTIVITY MAP</text><text x="32" y="59" font-size="18" fill="{p['ink']}">{total:,} contributions in the past year</text>
<g transform="translate(32 94)"><g fill="{p['muted']}" font-size="10">{month_svg}</g>{''.join(rects)}<g clip-path="url(#grid)"><g transform="translate(-60 0)"><animateTransform attributeName="transform" type="translate" from="-60 0" to="{grid_width+60} 0" dur="14s" repeatCount="indefinite"/><rect width="60" height="105" fill="url(#beam)"/><path d="M60 0V105" stroke="{p['accent']}" stroke-width="1" opacity=".6"/></g></g></g><text x="32" y="218" font-size="10" fill="{p['muted']}">{first} — {last} · Refreshed daily from GitHub</text><text x="946" y="218" text-anchor="end" font-size="10" fill="{p['accent']}">KEEP BUILDING ↗</text></g>'''
 return svg(w,236,content,'GitHub contribution calendar for hstkwow: '+str(total)+' contributions. A gentle animated scan crosses the real activity grid.')
def fetch():
 token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
 if not token:raise RuntimeError('GH_TOKEN is required, or supply --input with a saved API response')
 query='query { user(login: "hstkwow") { contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount color } } } } } }'
 req=urllib.request.Request('https://api.github.com/graphql',data=json.dumps({'query':query}).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'hstkwow-profile'})
 with urllib.request.urlopen(req,timeout=30) as response:return json.load(response)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path);args=parser.parse_args();data=json.loads(args.input.read_text()) if args.input else fetch()
 if data.get('errors'):raise RuntimeError('GitHub contribution query failed; previous assets are retained')
 calendar_data=data['data']['user']['contributionsCollection']['contributionCalendar'];target=ROOT/'assets';target.mkdir(exist_ok=True)
 outputs={}
 for mode,palette in PALETTES.items():outputs['intro-'+mode+'.svg']=banner(palette);outputs['activity-'+mode+'.svg']=calendar(calendar_data,palette)
 # Finish validation before replacing any existing files.
 from xml.etree import ElementTree as ET
 for content in outputs.values():ET.fromstring(content)
 for name,content in outputs.items():(target/name).write_text(content,encoding='utf-8')
 print('Generated four valid SVG assets from the GitHub contribution calendar.')
if __name__=='__main__':main()
