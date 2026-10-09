input("enter your first name")
input("enter your last name")
input("enter your birsth year")
input("enter your favorite program languige")
name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
birth_year = int(input("Enter your birth year: "))
favorite_language = input("Enter your favorite programming language: ")
name = name.upper()
last_name = last_name.upper()
favorite_language = favorite_language.upper()
age = 2026 - birth_year
is_adult = age >= 18
print(name, "|", last_name, "|", age, "|", favorite_language, "|", is_adult)
score = int(input("Enter the student's score (maximum 20 points): "))
grade = score // 2
print("The student's grade is:", grade)