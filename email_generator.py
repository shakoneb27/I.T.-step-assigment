# informaciis migeba
first_name = input("first name: ")
last_name = input("last name: ")
platform = input("choos platform(@gmail.com, @yahoo.com,@itstep.ge): ")
#monacmeebis damushaveba 
first_name = first_name.strip().lower()
last_name = last_name.strip().lower()
platform = platform.strip().lower()

first_two = first_name [:2] # saxelis pirveli 2 aso 

email = f"{first_two}{last_name}{platform}"  # f stringi ar var darwmunebuli sworad gamoviyene tu ara saba shemiswore 

print(f"your email is : {email}")
print("\n")
print("your email created")