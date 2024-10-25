"""
Tests for the abstract models.
Django-test-abstract-models copied from "github/myaser/7689869".
Modified by  H.Spierings ( importing models manually)

"""
# import datetime as dt
# from django.db import connection
from django.test import TestCase
from django.db import models, connection
# from django.db.migrations.executor import MigrationExecutor
# from django.db.migrations.state import ProjectState

from ..abstract_models import TimeStampedModel


class AbstractModelTest(TestCase):
    """ Testing of abstract models."""

    def setUp(self):
        """ Set up the project state and migrations for the dynamic model"""
        # self.executor = MigrationExecutor(connection)
        # self.old_state = self.executor._create_project_state()

        # Dynamically create a model that inherits from TimestampedModel
        self.TestModel = self.create_test_model()

    def create_test_model(self):
        """ Dynamical create and return a concrete model that inherits from TimeStampedModel."""
        class TestModel(TimeStampedModel):
            name = models.CharField(max_length=255)

            class Meta:
                app_label = 'tests'   # Use 'tests' app label to isolate it from actual app models.

        # Create the table for this temporary model using the migration system.
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestModel)

        return TestModel

    def tearDown(self) -> None:
        """ Clean up the dynamically created model's table"""
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(self.TestModel)

        # Restore the old project state
        # self.executor._migrate_all_forwards(
        #                   self.executor.loader.graph.leaf_nodes(), self.old_state)
        return super().tearDown()

    def test_inherits_abstract_fields(self):
        """ Test create an instance of the dynamically created model."""
        res = self.TestModel.objects.create(name='Test case')

        self.assertEqual(res.name, 'Test case')
        self.assertIsNotNone(res.created)
        self.assertIsNotNone(res.modified)
