from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://datathon_user:EeTXudLXaOtmBqLX0tKUhJ8kGWarqHTO@dpg-coc79mol6cac73er920g-a.singapore-postgres.render.com/datathon'
db = SQLAlchemy(app)

# Define your SQLAlchemy model
class Victim(db.Model):
    __tablename__ = 'tool5'

    district_name = db.Column(db.String(50), primary_key=True)
    unitname = db.Column(db.String(50))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    age = db.Column(db.Integer)
    profession = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    injurytype = db.Column(db.String(50))

# Define routes
@app.route('/crime_occurrence/<preference>', methods=['GET'])
def get_crime_occurrence(preference):
    # Analyze data based on preference
    if preference == 'age_group':
        # Example analysis by age group
        result = Victim.query.with_entities(Victim.age, db.func.count()).group_by(Victim.age).all()
        data = [{'age_group': item[0], 'crime_count': item[1]} for item in result]
    elif preference == 'sex':
        # Example analysis by sex
        result = Victim.query.with_entities(Victim.sex, db.func.count()).group_by(Victim.sex).all()
        data = [{'sex': item[0], 'crime_count': item[1]} for item in result]
    elif preference == 'location':
        # Example analysis by location (district name)
        result = Victim.query.with_entities(Victim.district_name, db.func.count()).group_by(Victim.district_name).all()
        data = [{'district_name': item[0], 'crime_count': item[1]} for item in result]
    else:
        return jsonify({'error': 'Invalid preference. Allowed values: age_group, sex, location'}), 400

    return jsonify(data), 200

@app.route('/crime_probability/<district>', methods=['GET'])
def get_crime_probability(district):
    # Calculate the probability of a crime occurring in the specified district
    crimes_in_district = Victim.query.filter_by(district_name=district).all()

    # Check if the district entered by the user exists in the dataset
    if not crimes_in_district:
        return jsonify({'error': f'District "{district}" not found in the dataset.'}), 404

    # Calculate the total number of crimes
    total_crimes = Victim.query.count()

    # Calculate the probability of a crime occurring in the specified district
    district_crime_probability = len(crimes_in_district) / total_crimes
    return jsonify({'district': district, 'crime_probability': district_crime_probability}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
