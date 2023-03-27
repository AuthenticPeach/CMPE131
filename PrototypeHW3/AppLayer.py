from domain_layer import RFP
from data_access_layer import RFPRepository

class RFPService:
    def __init__(self):
        self.rfp_repository = RFPRepository()

    def create_rfp(self, company_name, project_details, evaluation_criteria, submission_requirements):
        rfp = RFP(company_name, project_details, evaluation_criteria, submission_requirements)
        self.rfp_repository.create(rfp)