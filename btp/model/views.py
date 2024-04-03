from django.shortcuts import render
import csv
import requests
import json
# Create your views here.


def home(request):
    if request.method == 'POST' and request.FILES.get('csvfile'):
        input_file = request.FILES['csvfile']
        data_rows = []
        
        # Read the uploaded CSV file
        csv_content = input_file.read().decode('utf-8-sig')  
        csv_reader = csv.reader(csv_content.splitlines())
        
        for row in csv_reader:
            row_string = ','.join(row)
            data_rows.append(row_string)
        
        
        url = "https://v7qkzt8oi1.execute-api.us-east-1.amazonaws.com/stage1/dev" 
        payload="\n".join(data_rows)

        headers = {
        'Content-Type': 'text/csv'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = json.loads(response.text)
        ac=0
        nc=0
        prediction_strings = ['Abnormal' if pred == 1 else 'Normal' for pred in response_data["Prediction"]]
        for p in prediction_strings:
            if p=='Abnormal':
                ac+=1
            else:
                nc+=1
        
        context = {'predictions': enumerate(prediction_strings, start=1),'ac':ac,'nc':nc}
        return render(request, 'model/result.html',context)
    
    return render(request, 'model/home.html')