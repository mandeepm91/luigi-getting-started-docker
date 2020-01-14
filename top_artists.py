# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import random
from collections import defaultdict
from heapq import nlargest

from luigi import six
import luigi

class Streams(luigi.Task):
  """
  Faked version right now, just generates bogus data.
  """
  date = luigi.DateParameter()

  def run(self):
    """
    Generates bogus data and writes it into the :py:meth:`~.Streams.output` target.
    """
    with self.output().open('w') as output:
      for _ in range(1000):
        output.write('{} {} {}\n'.format(
          random.randint(0, 999),
          random.randint(0, 999),
          random.randint(0, 999)))

  def output(self):
    """
    Returns the target output for this task.
    In this case, a successful execution of this task will create a file in the local file system.

    :return: the target output for this task.
    :rtype: object (:py:class:`luigi.target.Target`)
    """
    return luigi.LocalTarget(self.date.strftime('/data/streams_%Y_%m_%d_faked.tsv'))


class AggregateArtists(luigi.Task):
  """
  This task runs over the target data returned by :py:meth:`~/.Streams.output` and
  writes the result into its :py:meth:`~.AggregateArtists.output` target (local file).
  """

  date_interval = luigi.DateIntervalParameter()

  def output(self):
    """
    Returns the target output for this task.
    In this case, a successful execution of this task will create a file on the local filesystem.

    :return: the target output for this task.
    :rtype: object (:py:class:`luigi.target.Target`)
    """
    return luigi.LocalTarget("/data/artist_streams_{}.tsv".format(self.date_interval))

  def requires(self):
    """
    This task's dependencies:

    * :py:class:`~.Streams`

    :return: list of object (:py:class:`luigi.task.Task`)
    """
    return [Streams(date) for date in self.date_interval]

  def run(self):
    artist_count = defaultdict(int)

    for t in self.input():
      with t.open('r') as in_file:
        for line in in_file:
          _, artist, track = line.strip().split()
          artist_count[artist] += 1

    with self.output().open('w') as out_file:
      for artist, count in six.iteritems(artist_count):
        out_file.write('{}\t{}\n'.format(artist, count))


class Top10Artists(luigi.Task):
  """
  This task runs over the target data returned by :py:meth:`~/.AggregateArtists.output` and
  writes the result into its :py:meth:`~.Top10Artists.output` target (a file in local filesystem).
  """
  date_interval = luigi.DateIntervalParameter()

  def requires(self):
    """
    This task's dependencies:

    * :py:class:`~.AggregateArtists`

    :return: object (:py:class:`luigi.task.Task`)
    """
    return AggregateArtists(self.date_interval)

  def output(self):
    """
    Returns the target output for this task.
    In this case, a successful execution of this task will create a file on the local filesystem.

    :return: the target output for this task.
    :rtype: object (:py:class:`luigi.target.Target`)
    """
    return luigi.LocalTarget("/data/top_artists_%s.tsv" % self.date_interval)

  def run(self):
    top_10 = nlargest(10, self._input_iterator())
    with self.output().open('w') as out_file:
      for streams, artist in top_10:
        out_line = '\t'.join([
          str(self.date_interval.date_a),
          str(self.date_interval.date_b),
          artist,
          str(streams)
        ])
        out_file.write((out_line + '\n'))

  def _input_iterator(self):
    with self.input().open('r') as in_file:
      for line in in_file:
        artist, streams = line.strip().split()
        yield int(streams), artist


if __name__ == "__main__":
  luigi.run()