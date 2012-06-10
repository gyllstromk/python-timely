Python Timely
=============

Stopwatch interface for Python. Currently supports two modes: timing execution (:class:`Stopwatch`), and pausing the completion of a block of code until a specified time has elapsed :class:`Blocker`.

Stopwatch usage
---------------

::
    with Stopwatch() as s:
        do_a()
        do_b()
        print s.duration() # time it took to execute do_a() and do_b()
        do_c()

    print s.duration() # time it took to execute do_a(), do_b(), and do_c()

    if s > 3: # comparators implicitly evaluate duration
        print 'took longer than 3 seconds'

Blocker usage
-------------

::

        with Blocker(3) as w:
            print 'Happens immediately!'
            time.sleep(1.5)  # executes immediately
            # ... we wait here until 3 seconds have passed

        print '3 seconds have passed!'
