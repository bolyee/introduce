from pathlib import Path
import json
from html import escape
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parent
D = json.loads((ROOT/'content.json').read_text())
e = lambda value: escape(str(value), quote=True)
def url(value):
    parsed = urlparse(value)
    if parsed.scheme not in ('', 'https', 'mailto') or value.startswith('//') or value == '#':
        raise ValueError('허용되지 않은 링크: ' + value)
    return e(value)
def links(items):
    return '<p class="links">' + ' · '.join(f'<a href="{url(x["url"])}">{e(x["label"])}</a>' for x in items) + '</p>' if items else ''
def media(items):
    result = ''
    for item in items:
        if item.get('approved') is not True:
            continue
        title = e(item['title'])
        body = ''
        if item.get('cover'):
            body += f'<img src="{url(item["cover"])}" alt="{title} 커버" loading="lazy">'
        if item.get('audio'):
            body += f'<audio controls preload="none" aria-label="{title}"><source src="{url(item["audio"])}">오디오 재생을 지원하는 브라우저가 필요합니다.</audio>'
        body += links(item.get('links', []))
        if body:
            if item.get('description'):
                body = f'<p class="muted">{e(item["description"])}</p>' + body
            result += f'<figure><figcaption>{title}</figcaption>{body}</figure>'
    return '<div class="media">' + result + '</div>' if result else ''
def section(id, title, body):
    return f'<section id="{id}" aria-labelledby="{id}-title"><h2 id="{id}-title">{title}</h2>{body}</section>'
projects = ''
for p in D['projects']:
    detail = ''.join(f'<li><strong>{e(h)}.</strong> {e(t)}</li>' for h,t in p['details'])
    projects += f'''<article id="{e(p['id'])}"><h3>{e(p['title'])}</h3><p>{e(p['summary'])}</p><p class="status">{e(p['status'])}</p><details><summary>자세히 보기<span class="sr-only">: {e(p['title'])}</span></summary><ul>{detail}</ul></details>{links(p['links'])}{media(p.get('demo', []))}</article>'''
experience = ''
for x in D['experience']:
    note = ' · ' + e(x['note']) if x.get('note') else ''
    experience += f'''<article><div class="entry-heading"><h3>{e(x['organization'])}</h3><span class="date">{e(x['period'])}</span></div><p class="role">{e(x['role'])}{note}</p><ul>{''.join('<li>'+e(t)+'</li>' for t in x['items'])}</ul>{links(x['links'])}</article>'''
a = D['education']
nav = ''.join(f'<a href="#{name.lower()}">{name}</a>' for name in ['About','Projects','Music','Experience','Education','Contact'])
about = ''.join(f'<p>{e(text)}</p>' for text in D['about'])
about += '<h3 class="subheading">Research Interests</h3><p class="muted">앞으로 탐구하고 싶은 주제입니다.</p><ul>' + ''.join(f'<li><strong>{e(h)}</strong> — {e(t)}</li>' for h,t in D['interests']) + '</ul>'
music = '<ul>' + ''.join(f'<li><strong>{e(h)}</strong> <span class="muted">({e(d)})</span><br>{e(t)}</li>' for d,h,t in D['music']) + '</ul>'
music += f'<p class="muted">사용 도구: {e(D["musicTools"])}</p>' + media(D['musicWorks'])
education = f'''<div class="entry-heading"><h3>{e(a['school'])}</h3><span class="date">{e(a['period'])}</span></div><p>{e(a['department'])}<br>전체 평점 {e(a['gpa'])}/4.5 · 전공 평점 {e(a['majorGpa'])}/4.5</p><ul><li><strong>주요 과목:</strong> {e(a['courses'])}</li><li><strong>교육 이수:</strong> {e(a['training'])}</li></ul>'''
contact = f'<p>이메일: <a href="mailto:{e(D["email"])}">{e(D["email"])}</a></p>'
html = f'''<!doctype html>
<html lang="ko">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(D['name'])} | 개인 홈페이지</title><meta name="description" content="{e(D['intro'])}"><meta name="theme-color" content="#ffffff"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="{e(D['name'])} | 개인 홈페이지"><meta property="og:description" content="{e(D['intro'])}"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"></head>
<body><a class="skip" href="#main">본문으로 건너뛰기</a>
<div class="page"><header class="profile"><img class="portrait" src="{url(D['portrait'])}" alt="이현중 증명사진" width="413" height="531"><div><h1>{e(D['name'])}</h1><p>{e(D['affiliation'])}<br>{e(D['graduation'])}</p><p><a href="mailto:{e(D['email'])}">{e(D['email'])}</a><br><a href="{url(D['github'])}">github.com/bolyee</a></p><p class="profile-links"><a href="#projects">프로젝트</a> · <a href="mailto:{e(D['email'])}">이메일 연락</a></p></div></header>
<nav aria-label="주요 탐색">{nav}</nav>
<main id="main" tabindex="-1">{section('about','About',about)}{section('projects','Projects',projects)}{section('music','Music',music)}{section('experience','Experience',experience)}{section('education','Education',education)}{section('contact','Contact',contact)}</main><footer><span>{e(D['name'])}</span></footer></div></body></html>'''
(ROOT/'site/index.html').write_text(html)
print(f'Generated {ROOT / "site/index.html"}')
