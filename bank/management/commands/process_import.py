# -*- coding: utf-8 -*-

"""
    Process import tasks
"""
from datetime import datetime
import html5lib


from django.core.management.base import BaseCommand
import djapian


from bank.models import ImportTask, Link


djapian.load_indexes()


class Command(BaseCommand):
    help = 'Process import tasks'
    user = None

    def process_custom_html(self, task):
        """
            Base html processor.
        """
        file_obj = task.file
        p = html5lib.HTMLParser(
            tree=html5lib.treebuilders.getTreeBuilder("lxml"), 
            namespaceHTMLElements=False
        )
        doc = p.parse(file_obj.read())
        _dt = False
        _links = []
        for e in doc.getroot().iter():
            if e.tag == "dt":
                _dt = True
                a = e.find("a")
                if a is not None and a.get("href"):
                    if len(a.get("href")) > 255:
                        continue
                    if Link.objects.filter(owner=self.user, href=a.get("href")[:255]).exists():
                        _dt = False
                        continue
                    _link = Link()
                    _link.href = a.get("href")
                    if a.text:
                        _link.title = a.text[:255]
                    if a.get("add_date"):
                        try:
                            _link.added = datetime.fromtimestamp(int(a.get("add_date")))
                        except:
                            pass
                    if a.get("tags"):
                        _link.description = ""
                        for tag in a.get("tags").split(","):
                            _link.description += u" #%s" % tag.strip()
                    _link.owner = self.user
                    _links.append(_link)
            if e.tag == 'dd' and _dt and e.text:
                _links[-1].description += "\n\n\n"
                _links[-1].description += e.text
        return _links

    def process_delicious(self, task):
        return self.process_custom_html(task)

    def process_google(self, task):
        return self.process_custom_html(task)

    def handle(self, *args, **options):
        for t in ImportTask.objects.filter(status=1).select_related("user"):
            t.status = 2
            t.save()
            self.user = t.user
            try:
                links = getattr(self, "process_" + t.from_source, lambda x: False)(t)
            except Exception, e:
                print e
                print
                t.status = 4
                t.save()
                continue
            if links:
                for link in links:
                    link.description = "%s\n\n\n#import_from_%s_%s" %(
                        link.description,
                        t.from_source,
                        t.pk
                    )
                    link.save()
                t.status = 3
                t.save()

        #self.stdout.write('Successfully processed')
