#!/usr/bin/python

# Makes the dir tree to put files into

import  os,sys

from process import process

from main.models import Client, Show, Location, Episode

class mkdirs(process):

  def mkdir(self,dir):
      """ makes the dir if it doesn't exist """
      ret = False
      print dir,
      if os.path.exists(dir):
         print '(exists)'
      else:
         if self.options.test:
             print '(testing, skipped)'
         else:
             os.makedirs(dir)
             ret = True
         print

      return ret

  def work(self):
        """
        find client and show, create the dirs
        """
        client = Client.objects.get(slug=self.options.client)
        show = Show.objects.get(client=client,slug=self.options.show)
        self.set_dirs(show)
        dirs = "dv tmp/dv titles webm mp4 txt thumb img mlt custom/titles custom/mlt"
        for d in dirs.split():
            full_dir = os.path.join(self.show_dir,d)
            ret = self.mkdir(full_dir)

        if self.options.raw_slugs:

    # get episodes for this show
            eps = Episode.objects.filter(show=show)
            for ep in eps:
                loc = ep.location.slug
                dt = ep.start.strftime("%Y-%m-%d")
                slug = ep.slug
                full_dir = os.path.join(self.show_dir,'dv',loc,dt,slug)
                ret = self.mkdir(full_dir)

        else:

    # get locations of the episodes
            for loc in Location.objects.filter(
                    show=show, active=True):
                 dir = os.path.join(self.show_dir,'dv',loc.slug)
                 ret = self.mkdir(dir)

        return

  def add_more_options(self, parser):
      parser.add_option('--raw-slugs', action="store_true",
                          help="Make a dir for each talk's raw files")

if __name__=='__main__': 
    p=mkdirs()
    p.main()

