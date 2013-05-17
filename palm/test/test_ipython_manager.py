from nose import SkipTest
import nose.tools
from palm.ipython_manager import IPythonManager

def remote_work_stub():
    return 0.0

def remote_work_with_args_stub(arg1, arg2):
    my_work = arg1 + arg2
    return my_work

@nose.tools.istest
class IPythonManagerTest(object):
    def setup(self):
        refresh_time = 0.1 # seconds
        self.task_manager = IPythonManager(refresh_time)
        try:
            self.task_manager.start()
        except:
            raise SkipTest
        self.num_tasks = 5

    def teardown(self):
        self.task_manager.stop()

    @nose.tools.istest
    def ipython_manager_runs_until_tasks_complete(self):
        self.setup()
        args = ()
        for i in xrange(self.num_tasks):
            self.task_manager.add_task(remote_work_stub)
        unfinished_tasks = self.task_manager.count_unfinished_tasks()
        nose.tools.eq_(unfinished_tasks, self.num_tasks,
                       msg="%d tasks sent to task manager." % unfinished_tasks)
        results = self.task_manager.collect_results_from_completed_tasks()
        unfinished_tasks = self.task_manager.count_unfinished_tasks()
        nose.tools.eq_(unfinished_tasks, 0,
                       msg="%d tasks are still running." % unfinished_tasks)
        self.teardown()
        print results

    @nose.tools.istest
    def ipython_manager_accepts_tasks_with_arguments(self):
        self.setup()
        for i in xrange(self.num_tasks):
            arg1 = i
            arg2 = i+1
            self.task_manager.add_task(remote_work_with_args_stub, arg1, arg2)
        unfinished_tasks = self.task_manager.count_unfinished_tasks()
        nose.tools.eq_(unfinished_tasks, self.num_tasks,
                       msg="%d tasks sent to task manager." % unfinished_tasks)
        results = self.task_manager.collect_results_from_completed_tasks()
        unfinished_tasks = self.task_manager.count_unfinished_tasks()
        nose.tools.eq_(unfinished_tasks, 0,
                       msg="%d tasks are still running." % unfinished_tasks)
        self.teardown()
        print results
