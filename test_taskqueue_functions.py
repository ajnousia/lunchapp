import unittest
import unclassified_functions

from google.appengine.api import taskqueue
from google.appengine.ext import testbed


class TaskQueueTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_taskqueue_stub()
        self.taskqueue_stub = self.testbed.get_stub(
            testbed.TASKQUEUE_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def testTaskAddedToQueue(self):
        taskqueue.Task(name="my_task", url="/url/of/my/task/").add()
        tasks = self.taskqueue_stub.get_filtered_tasks()
        assert len(tasks) == 1
        assert tasks[0].name == "my_task"

suite = unittest.TestLoader().loadTestsFromTestCase(TaskQueueTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
