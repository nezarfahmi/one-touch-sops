from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
  {
    'id' : 1,
    'name': 'Sales Engineer',
    'location' : 'Westfield, Indiana',
    'salary':'$100,000'
  },
  {
    'id':2,
    'name':'Electrician',
    'location' : 'Indianapolis, Indiana',
    'salary':'$75,000'
  },
  {
    'id':2,
    'name':'Frontend Engineer',
    'location':'Remote',
    'salary':'$105,000'
  },
  {
    'id':2,
    'name':'Backend Engineer',
    'location':'Remote',
    'salary':'$120,000'
  }
]

@app.route("/")
def hello_onetouch():
  return render_template("home.html", 
                         jobs=JOBS, company_name='One-Touch Automation')

@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)