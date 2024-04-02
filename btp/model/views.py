from django.shortcuts import render
import csv
import requests
# Create your views here.


def home(request):
    if request.method == 'POST' and request.FILES.get('csvfile'):
        input_file = request.FILES['csvfile']
        data_rows = []
        
        # Read the uploaded CSV file
        csv_content = input_file.read().decode('utf-8-sig')  # Remove BOM
        csv_reader = csv.reader(csv_content.splitlines())
        
        for row in csv_reader:
            row_string = ','.join(row)
            data_rows.append(row_string)
        
        print(data_rows)
        url = "" #to be added after deploying
        payload="\n".join(data_rows)

        headers = {
        'Content-Type': 'text/csv'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        return render(request, 'model/home.html', {'res': response.text})
    
    return render(request, 'model/home.html')