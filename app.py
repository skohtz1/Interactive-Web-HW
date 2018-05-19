import numpy as np
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

otu_id = Base.classes.otu
samples = Base.classes.samples
meta_data = Base.classes.samples_metadata

session = Session(engine)

##This doesn't work... 

# class Types(db.Model):
#     __tablename__ = 'otu'
#     id = db.Column(db.Integer, primary_key = True)
#     lowest_taxonomic_unit_found = db.Column(db.String)

#     def __repr__(self):
#         return '<Pet %r>' % (self.name)

# class Names(db.Model):
#     __tablename__ = "meta_data"
#     id = db.Column(db.Integer, primary_key = True)



# @app.before_first_request
# def setup():
#     db.create_all()


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

# Query the database and send the jsonified results
@app.route("/otu")
def types():
    results = session.query(otu_id.lowest_taxonomic_unit_found).all()
    print(results)
    all_types = list(np.ravel(results))
    return jsonify(all_types)


@app.route("/names")
def names():
    sample_names = []

    name_results = session.query(meta_data.SAMPLEID).all()
    for sample in name_results:
        sample_names.append("BB_"+str(sample[0]))

    # tried this..didnt work
    # samples_df = pd.read_sql_query(name_results, session.bind)
    # samples_df.set_index("otu_id",inplace = True)
    return jsonify(sample_names)

@app.route("/wfreq/<sample>")
def wfreq1(sample):
    sel2 = [meta_data.SAMPLEID,meta_data.WFREQ]
    results2 = session.query(*sel2).filter(meta_data.SAMPLEID ==sample[3:]).all()
    # wfreq_result = []

    # for item in results2:
    #     wrfreq_dict = {}
    #     wrfreq_dict["SAMPLEID"] = item[0]
    #     wrfreq_dict["WFREQ"] = 
    return jsonify(results2[0][1])

@app.route("/metadata/<sample>")
def samples_meta(sample):
    sel = [meta_data.SAMPLEID,meta_data.ETHNICITY,meta_data.GENDER,meta_data.AGE,meta_data.LOCATION,meta_data.BBTYPE]
    results = session.query(*sel).filter(meta_data.SAMPLEID ==sample[3:]).all()

    sample_results = []
    for sample in results:
        data_dict = {}
        data_dict["SAMPLEID"] = sample[0]
        data_dict["ETHNICITY"] = sample[1]
        data_dict["GENDER"] = sample[2]
        data_dict["AGE"] = sample[3]
        data_dict["LOCATION"] = sample[4]
        data_dict["BBTYPE"] = sample[5]
        sample_results.append(data_dict)
    return jsonify(sample_results)

@app.route("/samples/<sample>")
def sample_id(sample):
    sample_names = []

    name_results = session.query(meta_data.SAMPLEID).all()
    for sample1 in name_results:
        sample_names.append("BB_"+str(sample1[0]))

    sel = session.query(samples).all()
    otu_list = []
    sample_value_list = []
    sample_dict = {}
    for item in sel:
        selection_dict = item.__dict__
        otu_list.append(selection_dict["otu_id"])
        sample_value_list.append(selection_dict[sample])
    sample_dict["otu_id"] = otu_list
    sample_dict["samples_values"] = sample_value_list
    selection_df = pd.DataFrame.from_dict(sample_dict,orient = "columns",dtype = None)
    selection_df = selection_df.sort_values(by=["samples_values"],ascending=False)
    new_sample_dict = {}
    sample_values = selection_df["samples_values"].values.tolist()
    otu_id_values = selection_df["otu_id"].values.tolist()
    new_sample_dict["otu_id"] = otu_id_values
    new_sample_dict["sample_values"] = sample_values

    return jsonify(new_sample_dict)





if __name__ == '__main__':
    app.run(debug=True)


