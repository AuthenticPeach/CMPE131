from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rfp.db'
db = SQLAlchemy(app)

class RFP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50), nullable=False)
    project_details = db.Column(db.String(200), nullable=False)
    evaluation_criteria = db.Column(db.String(200), nullable=False)
    submission_requirements = db.Column(db.String(200), nullable=False)

    def __init__(self, company_name, project_details, evaluation_criteria, submission_requirements):
        self.company_name = company_name
        self.project_details = project_details
        self.evaluation_criteria = evaluation_criteria
        self.submission_requirements = submission_requirements

@app.route('/rfp', methods=['POST'])
def create_rfp():
    rfp_data = request.get_json()
    rfp = RFP(company_name=rfp_data['company_name'],
              project_details=rfp_data['project_details'],
              evaluation_criteria=rfp_data['evaluation_criteria'],
              submission_requirements=rfp_data['submission_requirements'])
    db.session.add(rfp)
    db.session.commit()
    return jsonify(rfp.id)

@app.route('/rfp', methods=['GET'])
def read_all_rfps():
    rfps = RFP.query.all()
    return jsonify([rfp.__dict__ for rfp in rfps])

@app.route('/rfp/<int:rfp_id>', methods=['GET'])
def read_rfp(rfp_id):
    rfp = RFP.query.get(rfp_id)
    if rfp is None:
        return jsonify({'error': 'RFP not found'}), 404
    return jsonify(rfp.__dict__)

@app.route('/rfp/<int:rfp_id>', methods=['PUT'])
def update_rfp(rfp_id):
    rfp_data = request.get_json()
    rfp = RFP.query.get(rfp_id)
    if rfp is None:
        return jsonify({'error': 'RFP not found'}), 404
    rfp.company_name = rfp_data['company_name']
    rfp.project_details = rfp_data['project_details']
    rfp.evaluation_criteria = rfp_data['evaluation_criteria']
    rfp.submission_requirements = rfp_data['submission_requirements']
    db.session.commit()
    return jsonify({'message': 'RFP updated successfully'})

@app.route('/rfp/<int:rfp_id>', methods=['DELETE'])
def delete_rfp(rfp_id):
    rfp = RFP.query.get(rfp_id)
    if rfp is None:
        return jsonify({'error': 'RFP not found'}), 404
    db.session.delete(rfp)
    db.session.commit()
    return jsonify({'message': 'RFP deleted successfully'})

if __name__ == '__main__':
    app.run()
