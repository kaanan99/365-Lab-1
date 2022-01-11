import numpy as np
import pandas as pd


def parse_file(file_name):
   df = pd.DataFrame({"S_Last":[], "S_First": [], "Grade": [], "Classroom":[], "Bus":[], "GPA": [], "T_Last":[], "T_First":[]})
   f = open(file_name)
   for line in f.readlines():
      df.loc[len(df.index)] = line.strip().split(",")
   f.close()
   df["Count"] = 1
   return df

def student_search(the_input, df):
   if len(the_input) == 2:
      temp = df[df["S_Last"] == the_input[1]]
      temp = temp[["S_Last", "S_First", "Grade", "Classroom", "T_Last", "T_First"]]
   elif len(the_input) == 3 and the_input[2] == "B":
      temp = df[df["S_Last"] == the_input[1]]
      temp = temp[["S_Last", "S_First", "Bus"]]
   else:
      return None
   return temp

def teacher_search(the_input, df):
   if len(the_input) == 2:
      temp = df[df["T_Last"] == the_input[1]]
      return temp[["S_Last", "S_First"]]
   else:
      return None
  
def grade_search(the_input, df):
   if len(the_input) == 2 or len(the_input) == 3:
      if int(the_input[1]) > 6 or int(the_input[1]) < 0:
         return None
   if len(the_input) == 2:
      temp = df[df["Grade"] == the_input[1]]
      return temp[["S_Last", "S_First"]]
   elif len(the_input) == 3:
      temp = df[df["Grade"] == the_input[1]]
      if the_input[2] == "H":
         temp = temp.sort_values(by=["GPA"], ascending=False)
         return pd.DataFrame(temp[["S_Last", "S_First", "GPA", "T_Last", "T_First", "Bus"]].iloc[0]).T
      elif the_input[2] == "L":
         temp = temp.sort_values(by=["GPA"], ascending=True)
         return pd.DataFrame(temp[["S_Last", "S_First", "GPA", "T_Last", "T_First", "Bus"]].iloc[0]).T
      else:
         return None
   else:
      return None

def average_search(the_input, df):
   if len(the_input) == 2 and int(the_input[1]) < 7 and int(the_input[1]) > 0:
      temp = df[df["Grade"] == the_input[1]]
      gpa = temp[["GPA"]].astype({"GPA":'float64'}).mean()
      return pd.DataFrame({"Grade":[the_input[1]], "GPA": gpa[0]})
   else:
      return None
   

def bus_search(the_input, df):
   if len(the_input) == 2:
      temp = df[df["Bus"] == the_input[1]]
      return temp[["S_Last", "S_First", "Grade", "Classroom"]]
   else:
      return None


def info(df):
   return df[["Grade", "Count"]].groupby("Grade").sum().reset_index()

def execute(the_input, df):
   if len(the_input) > 0:   
      first = the_input[0]
      if first == "S":
         new_df = student_search(the_input, df)
      elif first  == "T":
         new_df = teacher_search(the_input, df)
      elif first == "B":
         new_df = bus_search(the_input, df)
      elif first == "G":
         new_df = grade_search(the_input, df)
      elif first == "A":
         new_df = average_search(the_input, df)
      elif first == "I":
         new_df = info(df)
      elif first == "Q":
         return 0
      else:
         print("Invalid Command")
         return 1
      if new_df is None:
         print("Command Arguments Not Valid")
      elif new_df.shape[0] == 0:
         print("\nNo matching results found")
      else:
         print("\n")
         print(new_df.to_string(index = False))
   return 1

def main():
   df = parse_file('students.txt')
   quit = 1
   while quit != 0:
      user_input = input("Enter a Command: ").split()
      quit = execute(user_input, df)

if __name__ == '__main__':
   main()
