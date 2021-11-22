from django.test import TestCase

from analysis.tasks import simple_task


class TestCeleryTasks(TestCase):
    def test_simple_task(self):
        # with apply method executes the task synchronously and locally
        task = simple_task.s(1, 2).apply()
        self.assertEqual(task.status, 'SUCCESS')
        self.assertEqual(task.result, 3)
