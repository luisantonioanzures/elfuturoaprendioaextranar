
#!/usr/bin/env python3
"""Genera libro.epub desde contenido.json para GitHub Pages, sin dependencias externas.

Sólo las personas con permiso para editar el repositorio pueden publicar cambios.
"""
from __future__ import annotations

from datetime import datetime, timezone
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import json
import uuid
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TITLE = 'El futuro aprendió a extrañar'
AUTHOR = 'Luis Antonio Anzures González'
IDENTIFIER = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://luisantonioanzures.github.io/'))


class XHTMLSafe(HTMLParser):
    """Preserva formato básico del editor y convierte HTML a XHTML de EPUB3.
    Descarta scripts, estilos, atributos peligrosos e imágenes externas.
    """
    TAGS = {'p', 'strong', 'b', 'em', 'i', 'u', 'blockquote', 'ul', 'ol', 'li', 'h2', 'h3', 'br'}
    BLOCKED = {'script', 'style', 'iframe', 'object', 'svg'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.result: list[str] = []
        self.stack: list[str] = []
        self.blocked: list[str] = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if self.blocked:
            if tag in self.BLOCKED:
                self.blocked.append(tag)
            return
        if tag in self.BLOCKED:
            self.blocked.append(tag)
            return
        if tag == 'br':
            self.result.append('<br/>')
        elif tag in self.TAGS:
            self.result.append('<' + tag + '>')
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag.lower() != 'br':
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if self.blocked:
            if tag == self.blocked[-1]:
                self.blocked.pop()
            return
        if tag in self.stack:
            while self.stack:
                closing = self.stack.pop()
                self.result.append(f'</{closing}>')
                if closing == tag:
                    break

    def handle_data(self, data):
        if not self.blocked:
            self.result.append(escape(data, quote=False))

    def close(self):
        super().close()
        while self.stack:
            self.result.append(f'</{self.stack.pop()}>')


def clean_html(value: str) -> str:
    parser = XHTMLSafe()
    parser.feed(value if isinstance(value, str) else '')
    parser.close()
    result = ''.join(parser.result).strip()
    if not result:
        return '<p></p>'
    # Si sólo hay texto plano, lo tratamos como un párrafo legible.
    if not any(tag in result for tag in ('<p>', '<blockquote>', '<ul>', '<ol>', '<h2>', '<h3>')):
        return '<p>' + result + '</p>'
    return result


STYLE = '''@charset "UTF-8";
:root { color-scheme: light; }
html,body { margin: 0; padding: 0; background: #fff; color: #24211e; }
body { font-family: Georgia, "Iowan Old Style", "Palatino Linotype", Palatino, serif; font-size: 1em; line-height: 1.55; -webkit-hyphens: auto; hyphens: auto; }
h1 { font-weight: 400; line-height: 1.25; font-size: 1.65em; text-align: center; margin: 1.6em 0 1.35em; break-after: avoid; page-break-after: avoid; }
h2,h3 { break-after: avoid; font-weight: 500; }
p { margin: 0 0 1.05em; orphans: 2; widows: 2; }
blockquote { font-style: italic; text-align: center; margin: 2em 0; }
.chapter { padding: 0; margin: 0; }
.dedication { text-align: center; padding: 1em .6em; }
.dedication p { line-height: 1.7; text-align: center; }
.coverpage { margin: 0; padding: 0; text-align: center; page-break-after: always; break-after: page; }
.coverpage img { display: block; width: auto; height: auto; max-width: 100%; max-height: 98vh; margin: 0 auto; object-fit: contain; }
'''


def page(label: str, contents: str, klass='chapter') -> str:
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es">'
            '<head><meta charset="utf-8"/><title>' + escape(label) + '</title>'
            '<link rel="stylesheet" type="text/css" href="styles/book.css"/></head>'
            '<body><section class="' + klass + '"><h1>' + escape(label) + '</h1>'
            + contents + '</section></body></html>')


def build():
    data = json.loads((ROOT / 'contenido.json').read_text(encoding='utf-8'))
    chapters = data.get('capitulos') or []
    if not isinstance(chapters, list) or not chapters:
        raise ValueError('El libro necesita al menos un capítulo.')
    cover = (ROOT / 'portada.jpg').read_bytes()
    if not cover.startswith(b'\xff\xd8'):
        raise ValueError('La portada debe ser una imagen JPG válida.')

    files: list[tuple[str, str]] = [
        ('cover', 'cover.xhtml'), ('dedication', 'dedication.xhtml'), ('note', 'note.xhtml')
    ]
    pages = {
        'cover.xhtml': '<?xml version="1.0" encoding="utf-8"?>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es">'
            '<head><meta charset="utf-8"/><title>Portada</title>'
            '<link rel="stylesheet" type="text/css" href="styles/book.css"/></head>'
            '<body><section class="coverpage">'
            '<img src="images/cover.jpg" alt="Portada de El futuro aprendió a extrañar"/>'
            '</section></body></html>',
        'dedication.xhtml': page('Dedicatoria', clean_html(data.get('dedicatoria', '')), 'dedication'),
        'note.xhtml': page('Nota del autor', clean_html(data.get('nota', ''))),
    }
    for index, chapter in enumerate(chapters, 1):
        name = f'chapter{index}.xhtml'
        title = str(chapter.get('titulo') or f'Capítulo {index}').strip()
        pages[name] = page(title, clean_html(chapter.get('contenido', '')))
        files.append((f'chapter{index}', name))

    modified = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    manifest = ''.join(f'<item id="{i}" href="{name}" media-type="application/xhtml+xml"/>' for i, name in files)
    spine = ''.join(f'<itemref idref="{i}"/>' for i, _ in files)
    toc = ''.join(f'<li><a href="{name}">{escape("Portada" if i == "cover" else "Dedicatoria" if i == "dedication" else "Nota del autor" if i == "note" else str(chapters[int(i[7:])-1]["titulo"]))}</a></li>' for i, name in files)
    nav = ('<?xml version="1.0" encoding="utf-8"?>'
           '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="es">'
           '<head><title>Índice</title></head><body><nav epub:type="toc" id="toc"><h1>Índice</h1><ol>'
           + toc + '</ol></nav></body></html>')
    opf = ('<?xml version="1.0" encoding="utf-8"?>'
           '<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="pub-id" version="3.0" xml:lang="es">'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
           '<dc:identifier id="pub-id">' + IDENTIFIER + '</dc:identifier>'
           '<dc:title>' + escape(TITLE) + '</dc:title><dc:creator>' + escape(AUTHOR) + '</dc:creator>'
           '<dc:language>es</dc:language><dc:description>Para María Guadalupe y María de la Cruz.</dc:description>'
           '<meta property="dcterms:modified">' + modified + '</meta>'
           '<meta name="cover" content="cover-image"/></metadata><manifest>'
           + manifest
           + '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
           + '<item id="style" href="styles/book.css" media-type="text/css"/>'
           + '<item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>'
           '</manifest><spine>' + spine + '</spine></package>')
    container = ('<?xml version="1.0" encoding="utf-8"?>'
                 '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                 '<rootfiles><rootfile full-path="OEBPS/package.opf" '
                 'media-type="application/oebps-package+xml"/></rootfiles></container>')
    destination = ROOT / 'libro.epub'
    with zipfile.ZipFile(destination, 'w') as output:
        output.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        output.writestr('META-INF/container.xml', container, compress_type=zipfile.ZIP_DEFLATED)
        output.writestr('OEBPS/package.opf', opf, compress_type=zipfile.ZIP_DEFLATED)
        output.writestr('OEBPS/nav.xhtml', nav, compress_type=zipfile.ZIP_DEFLATED)
        output.writestr('OEBPS/styles/book.css', STYLE, compress_type=zipfile.ZIP_DEFLATED)
        output.writestr('OEBPS/images/cover.jpg', cover, compress_type=zipfile.ZIP_DEFLATED)
        for name, contents in pages.items():
            output.writestr('OEBPS/' + name, contents, compress_type=zipfile.ZIP_DEFLATED)
    print(f'EPUB generado: {destination.name}; {len(chapters)} capítulo(s).')


if __name__ == '__main__':
    build()
