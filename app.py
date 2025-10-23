from flask import Flask, render_template, request, redirect, url_for

# Import the DAL functions
from DAL import *

app = Flask(__name__)

# Initialize the database when the app starts
createDatabase()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/projects')
def projects():
    # Get all projects from the database
    projects = getAllProjects()
    return render_template('projects.html', projects=projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        # Get all projects to display current projects
        projects = getAllProjects()
        return render_template('contact.html', projects=projects)
    
    elif request.method == 'POST':
        # Get form data for new project
        title = request.form.get("title", "")
        description = request.form.get("description", "")
        image_filename = request.form.get("image_filename", "")
        technologies = request.form.get("technologies", "")
        github_link = request.form.get("github_link", "")
        demo_link = request.form.get("demo_link", "")
        
        # Save the project to database
        saveProjectDB(title, description, image_filename, technologies, github_link, demo_link)
        
        # Get updated projects list
        projects = getAllProjects()
        return render_template('contact.html', projects=projects, message="Project added successfully!")
    
    else:
        projects = getAllProjects()
        return render_template('contact.html', projects=projects, message='Something went wrong.')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)