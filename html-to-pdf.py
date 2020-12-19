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


os.chdir("C:\\Users\\Saranyu Technologies\\Desktop\\html-To-pdf")
print("current dir : " , os.getcwd())

report_date = []
reportTraffic_Total_speed = []
reportTraffic_In_speed = []
reportTraffic_Out_speed = []

holdAllDate = []
AverageData = []
SumsData = []
LowHighData = []
plotters = []
bandPlotName  = []
allSuperDate = []
groupLowHigh = []

rowData = []

url = "https://r2d2.nxtgen.com/ui/api1.0/perfreport/all"
payload = """{
    "category": "vCenter",
    "item": "172.16.64.100..HDDC..ESXi VM",
    "list": "Vikas-VM-N21A",
    "metrics": "CPU",
    "TimeZone": "Asia/Kolkata",
    "start_datetime": "2020-12-01 14:15",
    "end_datetime": "2020-12-15 14:15"
}"""

headers = {
  'sessionkey': 'bbc3634bdfeadeb0b0885f71ca1caebfe8fb1bde010e9738816a2753c33f457df4d2f8757522d0cc6c8eb9b940c3bca6c71c8b9b67eaf3434090c1520a290b4d',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, verify = False)

print(response.status_code , " response.status_code ", response)

if response.status_code == 200:
    reportData = response.json()
    rowData = response.json()
    
    SumsData = reportData['data']['Sums']
    LowHighData = reportData['data']['LowHigh']

    
    #     GRAPH START
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 7)
    fig.autofmt_xdate()
    
    indexzero = reportData['data']['plots'][0]
    del reportData['data']['plots'][0]
    RemovedTitle = reportData['data']['plots']

    print(rowData["plotters"])
    print(indexzero)
    for item in rowData["plotters"]:
        pos = indexzero.index(item)        
        tmpDate, tmpValue = [], []
        for j in RemovedTitle:
            tmpDate.append(j[0])
            tmpValue.append(j[pos])
        ax.plot(tmpDate, tmpValue, label=item)

    ax.set_ylabel('Mbit/s')
    ax.set_title('AutoIntelli Report')
    ax.legend()
    
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

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    tmpfile = BytesIO()
    plt.savefig(tmpfile, format='png')
    
    encoded = base64.b64encode(tmpfile.getvalue())
    plt.show()
       
    htmltemple = """
<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
    integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
  <title>Autointelli Report</title>
</head>

<body>


<div class="graph">
        <img src="data:image/png;base64,{{fig}}">
</div>

  <div class="SumsTable">
    <h2>Sums</h2>
    <table class="table table-striped">
      <tbody>
        {% for SumsTitle,SumsVal in reportData["data"]["Sums"].items() %}
        <tr>
          <td>{{SumsTitle}} | {{SumsVal}}</td>

        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <div class="AverageTable">
    <h2>Average</h2>
    <table class="table table-striped">
      <tbody>
        {% for AverageTitle,AverageVal in reportData["data"]["Average"].items() %}
        <tr>
          <td>{{AverageTitle}} | {{AverageVal}}</td>

        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <div class="LowHighTable">
    <h2>Low High</h2>
    <table class="table table-striped">
      <tbody>
        {% for LowHighTitle,LowHighVal in reportData["data"]["LowHigh"].items() %}
        <tr>
          <td>{{LowHighTitle}} | Low: {{LowHighVal["low"]}} | High: {{LowHighVal["high"]}}</td>

        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>


  <div class="rowData">
    <h2>Row Data</h2>
    <table class="table table-striped">
      <tbody>
        {% for key in reportData["data"]["plots"] %}
        <tr>
          {% for keys in key %}
          <td>{{keys}}</td>
          {% endfor %}
        </tr>
        {% endfor %}
      </tbody>
    </table>
    <div>
</body>
</html>
    """

             
    template = Template(htmltemple)
    
    template_render = template.render(
        fig = figdata_png.decode('utf8'),
        plotters = plotters,
        bandPlotName = bandPlotName,
        AverageData = AverageData,
        SumsData = SumsData,
        LowHighData = groupLowHigh,
        payload= json.loads(payload),
        reportData = rowData
    )
    
    options = {
        "enable-local-file-access": None,
        'margin-top': '0.50in',
        'margin-bottom': '0.50in',
        'margin-right': '0.10in',
        'margin-left': '0.10in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdfkit.from_string(template_render,'my_testpdf.pdf', options=options)
    print("PDF Generated...")
