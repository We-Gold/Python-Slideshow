from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
	templateData = {
      'paused' : False,
    }
	return render_template('index.html', **templateData)

@app.route("/<action>")
def action(action):
    if(action == "back"):
        templateData = {
            'paused' : False,
        }
        return render_template('index.html', **templateData)
    elif(action == "toggle_pause"):
        templateData = {
            'paused' : True,
        }
        return render_template('index.html', **templateData)
    elif(action == "skip"):
        templateData = {
            'paused' : False,
        }
        return render_template('index.html', **templateData)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)