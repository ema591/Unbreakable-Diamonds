# Import the app from the __init__.py file in quizaris package (which is a directory name)
from quizaris import app

# The value of __name__ returns '__main__', __name__ is a special variable which sets the variable value of 
# __name__ to __main__ if that file is the main file e.g. python3 quizaris.py will return __main__. 
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")