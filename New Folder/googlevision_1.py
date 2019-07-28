import os
import pickle




def main():

    while True:
        with open('person.ck', 'rb') as file:
            person = pickle.load(file)
        if person == "True":
            print("Complete!")
            break


if __name__ == '__main__':
    main()

   