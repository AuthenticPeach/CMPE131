from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///rfp.db', echo=True)
Base = declarative_base()

class RFPModel(Base):
    __tablename__ = 'rfp'

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    project_details = Column(String)
    evaluation_criteria = Column(String)
    submission_requirements = Column(String)

class RFPRepository:
    def __init__(self):
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create(self, rfp):
        rfp_model = RFPModel(company_name=rfp.company_name,
                             project_details=rfp.project_details,
                             evaluation_criteria=rfp.evaluation_criteria,
                             submission_requirements=rfp.submission_requirements)
        self.session.add(rfp_model)
        self.session.commit()

    def read_all(self):
        rfps = self.session.query(RFPModel).all()
        return [self._convert_to_rfp(rfp) for rfp in rfps]

    def read(self, rfp_id):
        rfp_model = self.session.query(RFPModel).filter_by(id=rfp_id).first()
        return self._convert_to_rfp(rfp_model)

    def update(self, rfp):
        rfp_model = self.session.query(RFPModel).filter_by(id=rfp.id).first()
        rfp_model.company_name = rfp.company_name
        rfp_model.project_details = rfp.project_details
        rfp_model.evaluation_criteria = rfp.evaluation_criteria
        rfp_model.submission_requirements = rfp.submission_requirements
        self.session.commit()

    def delete(self, rfp_id):
        rfp_model = self.session.query(RFPModel).filter_by(id=rfp_id).first()
        self.session.delete(rfp_model)
        self.session.commit()

    def _convert_to_rfp(self, rfp_model):
        if not rfp_model:
            return None
        return RFP(rfp_model.company_name,
                   rfp_model.project_details,
                   rfp_model.evaluation_criteria,
                   rfp_model.submission_requirements)

