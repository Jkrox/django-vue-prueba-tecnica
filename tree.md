.
├── backend
│   ├── api
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── models.cpython-312.pyc
│   │   │   ├── serializers.cpython-312.pyc
│   │   │   ├── tasks.cpython-312.pyc
│   │   │   ├── urls.cpython-312.pyc
│   │   │   └── views.cpython-312.pyc
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── blog
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── settings.cpython-312.pyc
│   │   │   └── urls.cpython-312.pyc
│   │   ├── asgi.py
│   │   ├── celery.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── Dockerfile
│   ├── manage.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_tasks.py
│   │   └── test_views.py
│   └── uv.lock
├── docker-compose.test.yml
├── docker-compose.yml
├── frontend
│   ├── cypress.config.js
│   ├── Dockerfile
│   ├── node_modules
│   ├── package.json
│   ├── src
│   │   ├── App.vue
│   │   ├── assets
│   │   │   └── styles
│   │   ├── components
│   │   │   ├── CommentForm.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   └── PostCard.vue
│   │   ├── main.js
│   │   ├── router
│   │   │   └── index.js
│   │   ├── services
│   │   │   └── api.js
│   │   └── views
│   │       ├── CategoriesView.vue
│   │       ├── HomeView.vue
│   │       ├── PostDetailView.vue
│   │       ├── PostsView.vue
│   │       └── TagsView.vue
│   ├── tests
│   │   ├── e2e
│   │   │   └── specs
│   │   └── unit
│   │       └── PostCard.spec.js
│   └── vite.config.js
├── Makefile
└── tree.md
