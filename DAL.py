# A. Import the sqlite library
import sqlite3

#######################################################
# 1. ADD PROJECT TO DB
#######################################################
def saveProjectDB(Title, Description, ImageFileName, Technologies="", GitHubLink="", DemoLink=""):
    #A. Make a connection to the database
    conn = None
    conn = sqlite3.connect("projects.db")

    #B. Write a SQL statement to insert a specific row (based on Title name)
    sql = 'INSERT INTO projects (Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink) values (?,?,?,?,?,?)'

    # B. Create a workspace (aka Cursor)
    cur = conn.cursor()

    # C. Run the SQL statement from above and pass it parameters for each ?
    cur.execute(sql, (Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink))

    # D. Save the changes
    conn.commit()
    if conn:
        conn.close()

#######################################################
# 2. SHOW PROJECTS IN A TABLE
#######################################################
#   THIS RETURNS AS LIST OF DICTIONARIES
def getAllProjects():
    # A. Connection to the database
    conn = sqlite3.connect('projects.db')

    # B. Create a workspace (aka Cursor)
    cursorObj = conn.cursor()

    # D. Run the SQL Select statement to retrieve the data
    cursorObj.execute('SELECT Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink FROM projects;')

    # E. Tell Python to 'fetch' all of the records and put them in
    #     a list called allRows
    allRows = cursorObj.fetchall()

    projectListOfDictionaries = []

    for individualRow in allRows:
        # Make sure we have an image name
        if individualRow[2] is not None and individualRow[2] != "":
            Image = individualRow[2]
        else:
            Image = "placeholder.png"
        
        # Create a dictionary for each row
        p = {
            "Title": individualRow[0], 
            "Description": individualRow[1], 
            "Image": Image,
            "Technologies": individualRow[3] if individualRow[3] else "",
            "GitHubLink": individualRow[4] if individualRow[4] else "",
            "DemoLink": individualRow[5] if individualRow[5] else ""
        }
        projectListOfDictionaries.append(p)

    if conn:
        conn.close()

    return projectListOfDictionaries

#######################################################
# 3. CREATE DATABASE AND TABLE
#######################################################
def createDatabase():
    # A. Make a connection to the database
    conn = sqlite3.connect("projects.db")
    
    # B. Create a workspace (aka Cursor)
    cur = conn.cursor()
    
    # C. Create the projects table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT NOT NULL,
            ImageFileName TEXT NOT NULL,
            Technologies TEXT,
            GitHubLink TEXT,
            DemoLink TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # D. Save the changes
    conn.commit()
    
    # E. Insert some sample data if table is empty
    cur.execute('SELECT COUNT(*) FROM projects')
    count = cur.fetchone()[0]
    
    if count == 0:
        # Insert sample projects
        sample_projects = [
            ("Golf Score Tracker", 
             "Created a score tracker for golf players allowing them to input their scores and compiling them into a database to track and compare with other players.",
             "project1.png",
             "VBA, VBA Macros",
             "https://github.com/Yjan11/personal-website/blob/main/K360-Capstone.xlsm",
             "K360-Capstone.xlsm"),
            ("Student Management Database", 
             "Created a database for managing students, which also includes the projects they manage and documents associated with them. Allows users to also assign teams for projects and enter new students into the system.",
             "project2.png",
             "HTML, CSS, Python",
             "https://github.com/Yjan11/personal-website/blob/main/Front-End%20Prototype%20Project%20Future.html",
             "Front-End Prototype Project Future.html")
        ]
        
        for project in sample_projects:
            cur.execute('''
                INSERT INTO projects (Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', project)
    
    conn.commit()
    if conn:
        conn.close()

