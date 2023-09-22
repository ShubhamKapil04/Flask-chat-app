
# Flask Socket.IO App README




## Introduction

This is a Flask web application that uses Socket.IO for real-time communication. This README provides information about the project, its setup, and how to run it.
## Prerequisites

Before running this Flask app, make sure you have the following installed:

* Python (3.6 or higher)
* Flask
* Flask-Socket.IO

You can install these dependencies using pip:

```bash
  pip install flask flask-socketio
```
## Project Structure

```
project-root/
│
├── main.py                 # Main application file
├── templates/             # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── room.html
|   ├── ...
|
├── static/                # Static files (CSS, JavaScript, etc.)
│   ├── styles.css
│   ├── ...
│
├── requirements.txt       # List of project dependencies
├── README.md              # This README file
```
## Usage/Examples

1. Clone the repository:
    ```bash
    git clone https://github.com/ShubhamKapil04/Flask-chat-app.git
    cd Flask-chat-app
    ```

2. Install the required packages:
    ``` bash
    pip install -r requirements.txt
    ```

3. Run the Flask app:
    ``` bash
    python main.py
    ```
4. Open your web browser and visit `http://localhost:5000` to access the application.

## Features

* Use the local server to communicate. And use the one to many communicate.
