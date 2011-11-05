# -*- coding: utf-8 -*-

"""
    Process exports tasks
"""
from time import mktime


from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.template.defaultfilters import escape


from bank.models import ExportTask, Link, HASHTAG_PATTERN


class Command(BaseCommand):
    help = 'Process export tasks'
    user = None

    def get_tags(self, body):
        if not body:
            return False
        return HASHTAG_PATTERN.findall(body)

    def process_bookmark(self, bookmark):
        tags = self.get_tags(bookmark.description)
        out = u"""<DT><A HREF="%(href)s" ADD_DATE="%(added)s" %(tags)s>%(title)s</A>\n"""
        out = out % {
            "href": bookmark.href,
            "added": mktime(bookmark.added.timetuple()) if bookmark.added else "",
            "tags": u'TAGS="%s"' % u",".join(tags) if tags else "",
            "title": escape(bookmark.title),
        }
        if bookmark.description:
            out += u"<DD>%s</DD>\n" % escape(bookmark.description)
        return out

    def process_start_html(self):
        return u"""
<!DOCTYPE NETSCAPE-Bookmark-file-1>
    <!--This is an automatically generated file.
    It will be read and overwritten.
    Do Not Edit! -->
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <Title>Bookmarks</Title>
    <H1>Bookmarks</H1>
    <DL><p>\n"""

    def process_end_html(self):
        return u"""</DL><p>"""

    def handle(self, *args, **options):
        for t in ExportTask.objects.filter(status=1).select_related("user"):
            t.status = 2
            t.save()
            try:
                out = []
                out.append(self.process_start_html())
                for i in Link.objects.filter(owner=t.user).order_by("added"):
                    out.append(self.process_bookmark(i))
                out.append(self.process_end_html())
                t.file.save("bookmarks_%s.html" % t.pk, ContentFile((u"".join(out)).encode("utf8")), save=True)
                t.status = 3
            except Exception:
                t.status = 4
            t.save()
