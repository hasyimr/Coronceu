from flask import Flask, render_template, url_for, request
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, validators, SubmitField
from wtforms.validators import DataRequired
import requests
from requests.exceptions import JSONDecodeError

app = Flask(__name__)
app.secret_key = "124qfsas"

class SearchForm(FlaskForm):

    nama_provinsi = StringField('Nama Provinsi', validators=[DataRequired()])
    submit = SubmitField('Search')




@app.route("/", methods=["POST", "GET"])
def home():
    form = SearchForm()
    methods = request.method
    
    if form.validate_on_submit():
        input_form = form.nama_provinsi.data.upper().split(" ")
        correct_format = "_".join(input_form)
        provinsi = correct_format
        url = f'https://data.covid19.go.id/public/api/prov_detail_{provinsi}.json'
        response = requests.get(url)
        try:
            data = response.json()
        except JSONDecodeError:
            data = "Not Found"
            return render_template("index.html", method=methods, data=data,form=form)
        else:
            data_list = [data['last_date'],data['kasus_total'], data['meninggal_dengan_tgl'] + data['meninggal_tanpa_tgl'], data['sembuh_dengan_tgl'] + data['sembuh_tanpa_tgl']]
            data_label = ["Tanggal Update","Total Kasus", "Total Meninggal", "Total Sembuh"]
            methods = request.method

            return render_template("index.html", method=methods, data=data, data_list=data_list, data_label=data_label, lenght=len(data_label), form=form)

    return render_template("index.html",form=form, method=methods)




if __name__ == "__main__":
    app.run(debug=True)