#!/usr/bin/env python3
"""Generate the self-hosted animated research banner. No API token is needed."""
from pathlib import Path
import html,math
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
def main():
 from xml.etree import ElementTree as ET
 target=ROOT/'assets';target.mkdir(exist_ok=True)
 for mode,palette in PALETTES.items():
  content=banner(palette);ET.fromstring(content)
  (target/('intro-'+mode+'.svg')).write_text(content,encoding='utf-8')
 print('Generated dark and light research banners.')
if __name__=='__main__':main()
