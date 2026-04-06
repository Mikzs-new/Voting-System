import requests

url = "http://127.0.0.1:8000/api/elections/8/"

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
#     'first_name': 'Cathrina',
#     'last_name': 'Fado',
#     'student_school_id': '2311600214',
#     'year_level': '3rd',
#     'email': 'cathrinafado@gmail.com',
#     'course': 2
# }

# response = requests.post(url, json=data)
# print(response.json())
