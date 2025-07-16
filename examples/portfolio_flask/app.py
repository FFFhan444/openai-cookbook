from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # simple session key

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'projects.json')

# Utility functions

def load_projects():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_projects(projects):
    with open(DATA_FILE, 'w') as f:
        json.dump(projects, f, indent=2)


def get_project(slug):
    for proj in load_projects():
        if proj.get('slug') == slug:
            return proj
    return None

# Public routes

@app.route('/')
def index():
    projects = [p for p in load_projects() if p.get('visible')]
    return render_template('index.html', projects=projects)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects/<slug>')
def project_detail(slug):
    project = get_project(slug)
    if not project or not project.get('visible'):
        return "Project not found", 404
    return render_template('detail.html', project=project)

# Admin routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


def login_required(func):
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper


@app.route('/admin')
@login_required
def dashboard():
    projects = load_projects()
    return render_template('dashboard.html', projects=projects)


@app.route('/admin/edit/<slug>', methods=['GET', 'POST'])
@login_required
def edit_project(slug):
    projects = load_projects()
    project = next((p for p in projects if p.get('slug') == slug), None)
    if request.method == 'POST':
        if not project:
            project = {'slug': slug}
            projects.append(project)
        project['title'] = request.form.get('title')
        project['image'] = request.form.get('image')
        project['description'] = request.form.get('description')
        project['tags'] = request.form.get('tags').split(',') if request.form.get('tags') else []
        project['visible'] = request.form.get('visible') == 'on'
        save_projects(projects)
        return redirect(url_for('dashboard'))
    return render_template('edit_project.html', project=project)


@app.route('/admin/delete/<slug>', methods=['POST'])
@login_required
def delete_project(slug):
    projects = load_projects()
    projects = [p for p in projects if p.get('slug') != slug]
    save_projects(projects)
    return redirect(url_for('dashboard'))


@app.route('/admin/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        slug = request.form.get('slug')
        projects = load_projects()
        if get_project(slug):
            return render_template('edit_project.html', error='Slug already exists')
        project = {
            'slug': slug,
            'title': request.form.get('title'),
            'image': request.form.get('image'),
            'description': request.form.get('description'),
            'tags': request.form.get('tags').split(',') if request.form.get('tags') else [],
            'visible': request.form.get('visible') == 'on'
        }
        projects.append(project)
        save_projects(projects)
        return redirect(url_for('dashboard'))
    return render_template('edit_project.html', project={})


if __name__ == '__main__':
    app.run(debug=True)
