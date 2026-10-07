from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cpi-data')
def get_cpi_data():
    csv_path = os.path.join(os.path.dirname(__file__), 'cpi_data.csv')
    
    if not os.path.exists(csv_path):
        return jsonify({"error": "cpi_data.csv not found. Run cpi_downloader.py first."}), 404

    try:
        # Skip title row
        df = pd.read_csv(csv_path, skiprows=1)
        
        labels = []
        monthly = []
        annual = []
        
        for _, row in df.iterrows():
            if len(row) >= 3 and pd.notna(row.iloc[0]):
                m_label = str(row.iloc[0]).strip()
                # Check for month patterns like 'Jan-24', 'Feb-24', etc.
                if any(m in m_label for m in ['Jan-', 'Feb-', 'Mar-', 'Apr-', 'May-', 'Jun-', 'Jul-', 'Aug-', 'Sep-', 'Oct-', 'Nov-', 'Dec-']):
                    try:
                        m_val = float(row.iloc[1]) if pd.notna(row.iloc[1]) else 0.0
                        a_val = float(row.iloc[2]) if pd.notna(row.iloc[2]) else 0.0
                        
                        labels.append(m_label)
                        monthly.append(m_val)
                        annual.append(a_val)
                    except ValueError:
                        continue

        return jsonify({
            "labels": labels,
            "monthly": monthly,
            "annual": annual
        })

    except Exception as e:
        return jsonify({"error": f"Parsing error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=4535)