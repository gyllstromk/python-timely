'''

    Python timely
    =============

    Simple stopwatch commands for timing and pausing code in Python.

    :copyright: (c) 2012 by Karl Gyllstrom
    :license: BSD (see LICENSE.txt)

'''

import time
import datetime


def now():
    ''' Current time. '''
    return datetime.datetime.utcnow()


def seconds_since(ts):
    ''' Seconds that have passed since ``now`` - ts. '''
    return seconds(now() - ts)


def seconds(ts):
    ''' Convert timedelta to seconds. '''

    seconds = ts.days * 24 * 60 * 60 + ts.seconds
    if ts.microseconds:
        return seconds + float(ts.microseconds) / 1000000
    return seconds


class _Base(object):
    def __enter__(self):
        self._start = now()
        return self


class Stopwatch(_Base):
    ''' Records time for a sequence of operations.  Use with 'with' statement.
    The duration recorded covers the span within the scope.

    The following illustrates an example of use::

        with Stopwatch() as s:
            do_a()
            do_b()
            print s.duration() # returns time it took to execute do_a() and do_b()
            do_c()
    
        print s.duration() # returns time it took to execute do_a(), do_b(), and do_c()

        if s > 3:
            print 'took longer than 3 seconds'

    '''

    def __init__(self):
        self._start = self._end = None
        self._ticks = []

    def __exit__(self, exc_type, exc_value, traceback):
        self._end = now()

    def __cmp__(self, value):
        return cmp(self.duration(), value)

    def tick(self):
        ''' Records time at the point it is called. This can be recovered via
        the :func:`ticks` call. Example usage::

            with Stopwatch() as s:
                do_a()
                s.tick()
                do_b()
                s.tick()

            print s.ticks()

        ::
            [<time of call 1 to s.tick()>, <time of call 2 to s.tick()>]

        '''

        self._ticks.append(now())

    def ticks(self):
        return self._ticks[:]

    def duration(self):
        ''' Returns duration of execution.  If called within block, returns
        duration since beginning of block. '''

        end = self._end
        if end is None:
            end = now()

        return seconds(end - self._start)


class Blocker(_Base):
    ''' Waits for inner operations to complete before allowing execution to finish::

        with Blocker(3) as w:
            print 'Happens immediately!'
            time.sleep(1.5)  # executes immediately
            # ... we wait here until 3 seconds have passed

        print '3 seconds have passed!'

    '''

    def __init__(self, duration):
        if isinstance(duration, datetime.datetime):
            duration = seconds(duration - now())
        elif isinstance(duration, datetime.timedelta):
            duration = seconds(duration)

        if duration < 0:
            raise ValueError('Can\'t wait for under 0 seconds')

        self._duration = duration
        self._start = None

    def __exit__(self, exc_type, exc_value, traceback):
        wait_for = self._duration - seconds(now() - self._start)

        if wait_for > 0:
            time.sleep(wait_for)
