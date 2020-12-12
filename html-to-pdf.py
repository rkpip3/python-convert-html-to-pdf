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
print(os.getcwd(), " : current dir ")

report_date = []
reportTraffic_Total_speed = []
reportTraffic_In_speed = []
reportTraffic_Out_speed = []
# allData = ''
holdAllDate = []

AverageData = []
SumsData = []
LowHighData = []

plotters = []
bandPlotName  = []

allSuperDate = []

groupLowHigh = []

url = "https://r2d2.nxtgen.com/ui/api1.0/perfreport/all"

payload="{\r\n    \"category\": \"Firewall\",\r\n    \"item\": \"\",\r\n    \"list\": \"10.225.11.20\",\r\n    \"metrics\": \"380..TommyHil-3021\",\r\n    \"TimeZone\": \"Asia/Kolkata\",\r\n    \"start_datetime\": \"2020-11-01 01:11\",\r\n    \"end_datetime\": \"2020-11-30 18:11\"\r\n}"
headers = {
  'sessionkey': 'bbc3634bdfeadeb0b0885f71ca1caebfe8fb1bde010e9738816a2753c33f457df4d2f8757522d0cc6c8eb9b940c3bca6c71c8b9b67eaf3434090c1520a290b4d',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, verify = False)

if response.status_code ==200:
    reportData = response.json()
    
    SumsData = reportData['data']['Sums']
    LowHighData = reportData['data']['LowHigh']
    
#     print(AverageData['Traffic Total(speed)'], ' AverageData')
    
    AverageData = {
        "Average" : [{
            "Traffic_Total_speed": reportData['data']['Average']['Traffic Total(speed)'],
            "Traffic_In_speed": reportData['data']['Average']['Traffic In(speed)'],
            "Traffic_Out_speed": reportData['data']['Average']['Traffic Out(speed)'],
            "Traffic_Total_volume": reportData['data']['Average']['Traffic Total(volume)'],
            "Traffic_In_volume": reportData['data']['Average']['Traffic In(volume)'],
            "Traffic_Out_volume": reportData['data']['Average']['Traffic Out(volume)']
        }]
    }
    
    SumsData = {
        "Sums" : [{
            "Traffic_Total_speed": reportData['data']['Sums']['Traffic Total(speed)'],
            "Traffic_In_speed": reportData['data']['Sums']['Traffic In(speed)'],
            "Traffic_Out_speed": reportData['data']['Sums']['Traffic Out(speed)'],
            "Traffic_Total_volume": reportData['data']['Sums']['Traffic Total(volume)'],
            "Traffic_In_volume": reportData['data']['Sums']['Traffic In(volume)'],
            "Traffic_Out_volume": reportData['data']['Sums']['Traffic Out(volume)']
        }]
    }
    
    LowHighData = reportData['data']['LowHigh']
#     print(LowHighData , ' LowHighData')
    for LH in reportData['data']['LowHigh'].items():
        LowHighDatad= {}

#         LowHighDatad = [{
#                 "name": LH[0],
#                 "low": LH[1]['low'],
#                 "high": LH[1]['high'],
#             }]
        
        LowHighDatad = {
            "mydate" : [{
                "name": LH[0],
                "low": LH[1]['low'],
                "high": LH[1]['high'],
            }]
        }
        groupLowHigh.append(LowHighDatad)
    
    print(groupLowHigh , ' LowHighDatad')
    
    
    plotsdata = reportData['data']
    plotters = reportData['plotters']
    bandPlotName = plotsdata['plots'][0]

    del plotsdata['plots'][0]

    allData = plotsdata['plots']
    figdata_png = ''

# print(allData , ' allData')

    for l in plotsdata['plots']:
        allSuperDate.append(l)
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
    
#     print(plotters , ' plotters')
#     print(bandPlotName , ' bandPlotName')
#     print(plotsdata['plots'] , ' allData')

#     dataframe = pd.read_csv("datafile-2.csv", index_col=0)

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
        'margin-top': '0.50in',
        'margin-bottom': '0.50in',
        'margin-right': '0.10in',
        'margin-left': '0.10in',
        'encoding': "UTF-8",
        'no-outline': None
    }


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
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"
        integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
    <title>Autointelli Report</title>

    <style>
        .graph {
            margin-bottom: 20px;
        }

        .graph img {
            display: block;
            margin: auto;
        }

        .fullTable {
            margin-top: 15px;
        }

        .table thead th {
            font-size: 12px !important;
        }

        .table td,
        .table th {
            font-size: 11px !important;
        }

        .h2,
        h2 {
            font-size: 15px;
            background-color: #ececec;
            padding: 10px 10px;
        }
    </style>

</head>

<body>

    <div class="graph">
        <img src="data:image/png;base64,{{fig}}">
    </div>

    <div class="row">
        <div class="col-md-4">
            <h2>Average</h2>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Traffic In(speed) Mbit/s</th>
                        <th scope="col">Traffic In(volume) MB</th>
                        <th scope="col">Traffic Out(speed) Mbit/s</th>
                        <th scope="col">Traffic Out(volume) MB</th>
                        <th scope="col">Traffic Total(speed) Mbit/s</th>
                        <th scope="col">Traffic Total(volume) MB</th>
                    </tr>
                </thead>
                <tbody>
                    {% for Avg in AverageData['Average'] %}
                    <tr>
                        <td>{{Avg['Traffic_Total_speed']}}</td>
                        <td>{{Avg['Traffic_In_speed']}}</td>
                        <td>{{Avg['Traffic_Out_speed']}}</td>
                        <td>{{Avg['Traffic_Total_volume']}}</td>
                        <td>{{Avg['Traffic_In_volume']}}</td>
                        <td>{{Avg['Traffic_Out_volume']}}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="col-md-4">
            <h2>Sum</h2>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Traffic In(speed) Mbit/s</th>
                        <th scope="col">Traffic In(volume) MB</th>
                        <th scope="col">Traffic Out(speed) Mbit/s</th>
                        <th scope="col">Traffic Out(volume) MB</th>
                        <th scope="col">Traffic Total(speed) Mbit/s</th>
                        <th scope="col">Traffic Total(volume) MB</th>
                    </tr>
                </thead>
                <tbody>
                    {% for sum in SumsData['Sums'] %}
                    <tr>
                        <td>{{sum['Traffic_Total_speed']}}</td>
                        <td>{{sum['Traffic_In_speed']}}</td>
                        <td>{{sum['Traffic_Out_speed']}}</td>
                        <td>{{sum['Traffic_Total_volume']}}</td>
                        <td>{{sum['Traffic_In_volume']}}</td>
                        <td>{{sum['Traffic_Out_volume']}}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="col-md-4">
            <h2>Low High</h2>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Name</th>
                        <th scope="col">High</th>
                        <th scope="col">Low</th>
                    </tr>
                </thead>
                <tbody>
                    {% for LowH in LowHighData %}
                    <tr>
                        <td>{{LowH['mydate'][0]['name']}}</td>
                        <td>{{LowH['mydate'][0]['low']}}</td>
                        <td>{{LowH['mydate'][0]['high']}}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <div class="fullTable">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">DateTime</th>
                    <th scope="col">Traffic Total(speed) Mbit/s</th>
                    <th scope="col">Traffic In(speed) Mbit/s</th>
                    <th scope="col">Traffic Out(speed) Mbit/s</th>
                    <th scope="col">Traffic Total(volume) MB</th>
                    <th scope="col">Traffic In(volume) MB</th>
                    <th scope="col">Traffic Out(volume) MB</th>
                </tr>
            </thead>
            <tbody>
                {% for employe in mydat %}
                <tr>
                    <td>{{employe[0]}}</td>
                    <td>{{employe[1]}}</td>
                    <td>{{employe[2]}}</td>
                    <td>{{employe[3]}}</td>
                    <td>{{employe[4]}}</td>
                    <td>{{employe[5]}}</td>
                    <td>{{employe[6]}}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
        integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous">
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous">
    </script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"
        integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous">
    </script>
</body>

</html> 
    """
    
    template = Template(htmltemple)
    
    template_render = template.render(
        mydat = allData,
        fig = figdata_png.decode('utf8'),
        plotters = plotters,
        bandPlotName = bandPlotName,
        allData = allData,
        AverageData = AverageData,
        SumsData = SumsData,
        LowHighData = groupLowHigh)

    pdfkit.from_string(template_render,'my_testpdf.pdf', options=options)
    print("PDF Generated...")
