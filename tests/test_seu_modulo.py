import unittest
from main import app
import sqlite3

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Inicializa um banco de dados em memória para testes
        with sqlite3.connect(':memory:') as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)')

    def test_add_valid_task(self):
        response = self.app.post('/add', data={'task': 'Nova tarefa'})
        self.assertEqual(response.status_code, 302)  # Verifica se redireciona
        with sqlite3.connect(':memory:') as conn:
            cursor = conn.execute('SELECT * FROM tasks WHERE task = ?', ('Nova tarefa',))
            task = cursor.fetchone()
            self.assertIsNotNone(task)  # Verifica se a tarefa foi adicionada

    def test_add_empty_task(self):
        response = self.app.post('/add', data={'task': ''})
        self.assertEqual(response.status_code, 302)  # Verifica se redireciona
        with sqlite3.connect(':memory:') as conn:
            cursor = conn.execute('SELECT * FROM tasks')
            tasks = cursor.fetchall()
            self.assertEqual(len(tasks), 0)  # Verifica se nenhuma tarefa foi adicionada

    def test_add_duplicate_task(self):
        self.app.post('/add', data={'task': 'Tarefa duplicada'})
        response = self.app.post('/add', data={'task': 'Tarefa duplicada'})
        self.assertEqual(response.status_code, 302)  # Verifica se redireciona
        with sqlite3.connect(':memory:') as conn:
            cursor = conn.execute('SELECT * FROM tasks WHERE task = ?', ('Tarefa duplicada',))
            tasks = cursor.fetchall()
            self.assertEqual(len(tasks), 2)  # Verifica se a tarefa duplicada foi adicionada

    def test_add_special_characters(self):
        response = self.app.post('/add', data={'task': '!@#$%^&*()'})
        self.assertEqual(response.status_code, 302)  # Verifica se redireciona
        with sqlite3.connect(':memory:') as conn:
            cursor = conn.execute('SELECT * FROM tasks WHERE task = ?', ('!@#$%^&*()',))
            task = cursor.fetchone()
            self.assertIsNotNone(task)  # Verifica se a tarefa com caracteres especiais foi adicionada

    def test_add_task_redirects(self):
        response = self.app.post('/add', data={'task': 'Outra tarefa'})
        self.assertEqual(response.status_code, 302)  # Verifica se redireciona
        self.assertIn(b'/', response.data)  # Verifica se a resposta contém a URL para redirecionamento

if __name__ == '__main__':
    unittest.main()
