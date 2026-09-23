"""Tests applicatifs HTTPS : aucune connexion directe Django/PostgreSQL."""
import http.cookiejar
import json
import re
import ssl
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import (Request, build_opener, HTTPSHandler,
                            HTTPCookieProcessor, ProxyHandler, HTTPRedirectHandler)

BASE = 'https://localhost:8443'


class LocalRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        require_local_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def require_local_url(url):
    assert urlsplit(url).scheme == 'https' and urlsplit(url).netloc == 'localhost:8443', url


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.texts, self.attrs = [], []
        self.feed(html)

    def handle_data(self, data):
        self.texts.append(data)

    def handle_starttag(self, tag, attrs):
        self.attrs.append((tag, dict(attrs)))


class DemoBrowser:
    def __init__(self, ca):
        self.jar = http.cookiejar.CookieJar()
        self.opener = build_opener(ProxyHandler({}), LocalRedirect(),
            HTTPSHandler(context=ssl.create_default_context(cafile=ca)),
            HTTPCookieProcessor(self.jar))

    def get(self, path, data=None):
        url = urljoin(BASE, path)
        require_local_url(url)
        headers = {'Origin': BASE, 'Referer': BASE + '/fr/'}
        if data is not None:
            data = dict(data)
            data['csrfmiddlewaretoken'] = next(c.value for c in self.jar if c.name == 'csrftoken')
        req = Request(url, data=urlencode(data).encode() if data is not None else None, headers=headers)
        with self.opener.open(req, timeout=20) as response:
            require_local_url(response.url)
            assert response.status == 200
            return response.read().decode(), response.url

    def login(self, username='demo.climb'):
        self.get('/fr/auth/login/')
        html, url = self.get('/fr/auth/login/', {'username': username, 'password': 'demo-mcl'})
        assert '/core/home/' in url, url
        assert any(c.name == 'sessionid' and c.secure for c in self.jar)
        return html


def check_demo(ca):
    client = DemoBrowser(ca)
    home = client.login()
    assert 'Démo' in home
    gyms, _ = client.get('/fr/core/list/?force_list=1')
    for name in ('Démo Voie', 'Démo Bloc', 'Démo Mixte'):
        assert name in gyms, name
    for gym, bloc, count in [(9001, False, 7), (9002, True, 6), (9003, False, 4)]:
        html, _ = client.get(f'/fr/core/guidebook/?salle_id={gym}&bloc={str(bloc).lower()}&map_display=True')
        rows = [a for t, a in Page(html).attrs if t == 'tr' and 'data-id' in a]
        assert len(rows) == count, (gym, len(rows))
        svg, _ = client.get(f'/static/core/media/map/{gym}.svg')
        assert 'PLAN FICTIF' in svg and 'circle' in svg
    projects, _ = client.get('/fr/core/projects/')
    ids = {a['data-ouverture-id'] for t,a in Page(projects).attrs if 'data-ouverture-id' in a}
    assert ids == {'900101','900102','900201'}, ids
    for bloc in ('false', 'true'):
        html, _ = client.get('/fr/core/logbook/?bloc='+bloc)
        assert 'Démo' in html
    history, _ = client.get('/fr/core/logbook/?bloc=false')
    assert 'Souvenir démonté' in history
    for mode in ('lead', 'flash'):
        html, _ = client.get('/fr/core/logbook/?mode='+mode)
        assert 'Démo' in html
    manifest, _ = client.get('/manifest.json')
    assert json.loads(manifest)['start_url'] == '/'
    sw, _ = client.get('/service-worker.js')
    assert 'myclimbinglist.app' not in sw
    print('OK HTTPS : login, accueil, 3 salles, 3 plans, topo voie/bloc, carnet, flash/tête, projets A/B/C, PWA.')
    return client
