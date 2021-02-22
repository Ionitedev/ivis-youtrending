from app import app, csv_data, group_assessment, test_data
from flask import render_template, request, session, redirect

@app.route('/')
def test():
    return str(test_data[:3])

@app.route('/index', methods=['GET', 'POST'])
def index_page():
    # default page
    if request.method == 'GET':
        return render_template('index.html', data=csv_data, attr_checked=range(12, 24), entity_checked=[])
    
    # ordered page
    entity_checked = list(map(int, request.form.getlist('member')))
    attr_checked = list(map(int, request.form.getlist('skill')))
    data = csv_data
    if 'order' in request.form:
        data = [data[0]] + sorted(data[1:], key=lambda x: int(x[int(request.form['order'])]), reverse=True)
        return render_template('index.html', data=data, attr_checked=attr_checked, entity_checked=entity_checked)
    else:
        return redirect('group', code=307)

@app.route('/person', methods=['GET'])
def person_page():
    id = request.args.get('id')
    return render_template('person.html', data=csv_data[int(id)], questions=csv_data[0])

@app.route('/group', methods=['POST'])
def group():
    members = list(map(int, request.form.getlist('member')))
    skills = list(map(int, request.form.getlist('skill')))

    if len(members) < 4 or len(members) > 5:
        return '<h2>You should choose 4 or 5 group members</h2>'

    if len(skills) < 1:
        return '<h2>You should choose at least one skill</h2>'

    assess, scp = group_assessment.assessment(members, skills)
    return render_template('group.html', assess=assess, members=[(csv_data[i][1], i) for i in members], scp=scp, recommended=max(scp, key=scp.get))