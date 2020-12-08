import os
import pdfkit
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.pyplot import figure
import requests
import json
import ssl 
import pandas as pd
import matplotlib as mlp
from __future__ import print_function
from jinja2 import Template
import base64
from io import BytesIO
import matplotlib.pyplot as plt, mpld3


os.chdir("E:\\exprotToPdf\\")
print(os.getcwd(), " : current dir ")

report_date = []
reportTraffic_Total_speed = []
reportTraffic_In_speed = []
reportTraffic_Out_speed = []
allData = []

holdAllDate = []

url = "https://r2d2.nxtgen.com/ui/api1.0/perfreport/all"

payload="{\r\n    \"category\": \"Firewall\",\r\n    \"item\": \"\",\r\n    \"list\": \"10.225.11.20\",\r\n    \"metrics\": \"380..TommyHil-3021\",\r\n    \"TimeZone\": \"Asia/Kolkata\",\r\n    \"start_datetime\": \"2020-11-01 01:11\",\r\n    \"end_datetime\": \"2020-11-30 18:11\"\r\n}"
headers = {
  'sessionkey': 'bbc3634bdfeadeb0b0885f71ca1caebfe8fb1bde010e9738816a2753c33f457df4d2f8757522d0cc6c8eb9b940c3bca6c71c8b9b67eaf3434090c1520a290b4d',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, verify = False)
reportData = response.json()
plotsdata = reportData['data']

del plotsdata['plots'][0]

allData = plotsdata['plots']
figdata_png = ''

# print(allData , ' allData')

for l in plotsdata['plots']:
    report_date.append(l[0])
    reportTraffic_Total_speed.append(l[1])
    reportTraffic_In_speed.append(l[2])
    reportTraffic_Out_speed.append(l[3])

holdAllDate = {
    "mydate" : [{
        "allData":allData
    }]
}


# print(holdAllDate , ' holdAllDate')

if response.status_code ==200:
    
    dataframe = pd.read_csv("datafile-2.csv", index_col=0)
    # print(dataframe.head(5))
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 7)
    fig.autofmt_xdate()
    ax.bar(report_date, reportTraffic_Total_speed)
    ax = plt.gca()
    plt.xticks(rotation=70)
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)  
#     plt.savefig('datagraph.jpg',dpi=100)
#     plt.fig_to_html()
#     print(plt.fig_to_html())
    
    
    options = {
        "enable-local-file-access": None,
        'margin-top': '0.10in',
        'margin-right': '0.10in',
        'margin-bottom': '0.10in',
        'margin-left': '0.10in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    # pdfkit.from_url('http://localhost/reports/reports.html','my_testpdf.pdf', options=options)

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
#     print(figdata_png, ' figdata_png')
    
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    
    encoded = base64.b64encode(tmpfile.getvalue())
    
    
    htmltemple = """
    <!doctype html>
    <html lang="en">
      <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
        <title>Autointelli Report</title>
      </head>
      <body>
        <img src="data:image/png;base64,{{fig}}">
         <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">Date</th>
              <th scope="col">reportTraffic_Total_speed</th>
              <th scope="col">reportTraffic_In_speed</th>
            </tr>
          </thead>
          <tbody>
          {% for employe in mydat %}
            <tr>
              <td>{{employe[0]}}</td>
              <td>{{employe[1]}}</td>
              <td>{{employe[2]}}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        <!-- Optional JavaScript; choose one of the two! -->
        <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper) -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>
        <!-- Option 2: jQuery, Popper.js, and Bootstrap JS
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.min.js" integrity="sha384-w1Q4orYjBQndcko6MimVbzY0tgp4pWB4lZ7lr30WKz0vr/aWKhXdBNmNb5D92v7s" crossorigin="anonymous"></script>
         <script src="https://cdnjs.cloudflare.com/ajax/libs/c3/0.7.20/c3.min.js"></script>
      </body>
    </html>
    """
    template = Template(htmltemple)

    template_render = template.render(mydat = allData, fig = figdata_png.decode('utf8') )
    pdfkit.from_string(template_render,'my_testpdf.pdf', options=options)
    print("PDF Generated...")
