from models import db, Qualification
import pandas as pd

def run():
    qualifications_df = pd.read_csv("utils/csv/dut_qualifications.csv")
    
    for _, row in qualifications_df.iterrows():
        q_name = row['qualification_name']
        q_code = row['qualification_code']
    
        new_qualification = Qualification(name=q_name, code=q_code)
        db.session.add(new_qualification)
    
    db.session.commit()