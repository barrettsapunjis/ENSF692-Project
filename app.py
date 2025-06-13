from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load CSV once on startup (replace with your CSV file path)
df = pd.read_csv('skaters.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    filtered_data = None
    keyword1 = ''
    keyword2 = ''

    if request.method == 'POST':
        keyword1 = request.form.get('keyword1', '').strip()
        keyword2 = request.form.get('keyword2', '').strip()

        # Simple filtering on two columns (replace 'Column1' and 'Column2')
        filtered = df

        if keyword1:
            filtered = filtered[filtered['position'].astype(str).str.contains(keyword1, case=False, na=False)]
        if keyword2:
            filtered = filtered[filtered['team'].astype(str).str.contains(keyword2, case=False, na=False)]

        filtered_data = filtered.to_string(index=False)


    return render_template('index.html', table=filtered_data, keyword1=keyword1, keyword2=keyword2)


