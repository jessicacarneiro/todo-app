from todo import app, tasks
import json

def test_main_page_returns_200():
        app.config['TESTING'] = True
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200

def test_list_tasks_should_return_200():
    app.config['TESTING'] = True
    with app.test_client() as client:
        response = client.get('/tasks')
        assert response.status_code == 200

def test_create_task_with_post():
    with app.test_client() as client:
        response = client.post('/tasks', data=json.dumps({
        'title': 'task 1',
        'description': 'my first task'}),
        content_type='application/json')
        assert response.status_code != 405

def test_create_task_returns_new_task():
    tasks.clear()
    client = app.test_client()
    response = client.post('/tasks', data=json.dumps({
        'title': 'task 1',
        'description': 'my first task'}),
        content_type='application/json')
    data = json.loads(response.data.decode('utf-8'))
    assert data['id'] == 1
    assert data['title'] == 'task 1'
    assert data['description'] == 'my first task'
    assert data['status'] is False

def test_create_task_should_return_201():
    with app.test_client() as client:
        response = client.post('/tasks', data=json.dumps({
            'title': 'task 1',
            'description': 'my first task'}),
            content_type='application/json')
        assert response.status_code == 201

def test_create_task_insert_entry_database():
    tasks.clear()
    client = app.test_client()
    client.post('/tasks', data=json.dumps({
            'title': 'task 1',
            'description': 'my first task'}),
            content_type='application/json')
    assert len(tasks) > 0

def test_create_task_without_description():
    client = app.test_client()
    response = client.post('/tasks', data=json.dumps({
        'title': 'task 1'}),
        content_type='application/json')
    assert response.status_code == 400

def test_create_task_without_title():
    client = app.test_client()
    response = client.post('/tasks', data=json.dumps({
        'description': 'my first task'}),
        content_type='application/json')
    assert response.status_code == 400

def test_detail_existing_task():
        tasks.clear()
        tasks.append({
                'id': 1,
                'title': 'task 1',
                'description': 'my first task',
                'status': False
        })
        client = app.test_client()
        response = client.get('/tasks/1', content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200
        assert data['id'] == 1
        assert data['title'] == 'task 1'
        assert data['description'] == 'my first task'
        assert data['status'] is False

def test_detail_nonexisting_task():
        tasks.clear()
        client = app.test_client()
        response = client.get('/tasks/1', content_type='application/json')
        assert response.status_code == 404

def test_updating_exiting_task():
        tasks.clear()
        tasks.append({
                'id': 1,
                'title': 'task 1',
                'description': 'my first task',
                'status': False
        })
        client = app.test_client()
        response = client.put('/tasks/1', data=json.dumps({
                'title': 'updated title',
                'description': 'updated description',
                'status': True
                }
        ), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))
        assert response.status_code == 200
        assert data['id'] == 1
        assert data['title'] == 'updated title'
        assert data['description'] == 'updated description'
        assert data['status'] is True

def test_updating_nonexiting_task():
        tasks.clear()
        client = app.test_client()
        response = client.put('/tasks/1', data=json.dumps({
                'title': 'updated title',
                'description': 'updated description',
                'status': True
                }
        ), content_type='application/json')
        assert response.status_code == 404

def test_update_task_with_invalide_fields():
        tasks.clear()
        tasks.append({
                'id': 1,
                'title': 'task 1',
                'description': 'my first task',
                'status': False
        })
        client = app.test_client()
        # without status
        response = client.put('/tasks/1', data=json.dumps({
                'title': 'updated title',
                'description': 'updated description'
                }
        ), content_type='application/json')
        assert response.status_code == 400
        # without title
        response = client.put('/tasks/1', data=json.dumps({
                'description': 'updated description',
                'status': True
                }
        ), content_type='application/json')
        assert response.status_code == 400
        # without description
        response = client.put('/tasks/1', data=json.dumps({
                'title': 'updated title',
                'status': True
                }
        ), content_type='application/json')
        assert response.status_code == 400

def test_content_type_index_route():
        client = app.test_client()
        response = client.get('/')
        assert 'text/html' in response.content_type

def test_content_type_add_route():
        client = app.test_client()
        response = client.get('/add')
        assert 'text/html' in response.content_type

def test_content_type_login_route():
        client = app.test_client()
        response = client.get('/login')
        assert 'text/html' in response.content_type