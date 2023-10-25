from models import db, Module
import pandas as pd

def run():
    modules_df = pd.read_csv("utils/csv/dut_modules.csv")

    for _, row in modules_df.iterrows():
        module_name = row['module_name']
        module_code = row['module_code']

        new_module = Module(name=module_name, code=module_code)
        db.session.add(new_module)

    db.session.commit()