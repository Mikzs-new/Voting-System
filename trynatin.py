import requests

url = "http://127.0.0.1:8000/api/students/8/"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # if type(data) is list:
    #     for student in data:
    #         print(f'{student['id']} - {student['first_name']} {student['last_name']} - {student['student_school_id']} - {student['course']} - {student['year_level']} - {student['email']}') 
    # else:
    print(data)
else:
    print("Error:", response.status_code)

# data = {
#     'name': 'Bachelor of Science in Civil Engineering',
# }

# response = requests.post(url, json=data)
# print(response.json())
