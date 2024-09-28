import unittest
import sqlite3
from main import app


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = sqlite3.connect('test_todo.db')
        cls.connection.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)')

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        self.connection.execute('DELETE FROM tasks')  # Limpa a tabela antes de cada teste

    def test_add_valid_task(self):
        with self.connection:
            self.connection.execute('INSERT INTO tasks (task) VALUES (?)', ('Nova tarefa',))
        cursor = self.connection.execute('SELECT * FROM tasks WHERE task = ?', ('Nova tarefa',))
        task = cursor.fetchone()
        self.assertIsNotNone(task)

    def test_add_empty_task(self):
        with self.connection:
            self.connection.execute('INSERT INTO tasks (task) VALUES (?)', ('',))
        cursor = self.connection.execute('SELECT * FROM tasks WHERE task = ?', ('',))
        task = cursor.fetchone()
        self.assertIsNotNone(task)

    def test_add_duplicate_task(self):
        with self.connection:
            self.connection.execute('INSERT INTO tasks (task) VALUES (?)', ('Tarefa duplicada',))
            self.connection.execute('INSERT INTO tasks (task) VALUES (?)', ('Tarefa duplicada',))
        cursor = self.connection.execute('SELECT COUNT(*) FROM tasks WHERE task = ?', ('Tarefa duplicada',))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 2)

    def test_add_special_characters(self):
        with self.connection:
            self.connection.execute('INSERT INTO tasks (task) VALUES (?)', ('!@#$%^&*()',))
        cursor = self.connection.execute('SELECT * FROM tasks WHERE task = ?', ('!@#$%^&*()',))
        task = cursor.fetchone()
        self.assertIsNotNone(task)

    def test_task_count(self):
        with self.connection:
            self.connection.execute('INSERT INTO tasks (task) VALUES (?)', ('Tarefa 1',))
            self.connection.execute('INSERT INTO tasks (task) VALUES (?)', ('Tarefa 2',))
        cursor = self.connection.execute('SELECT COUNT(*) FROM tasks')
        count = cursor.fetchone()[0]
        self.assertEqual(count, 2)

if __name__ == '__main__':
    unittest.main()
