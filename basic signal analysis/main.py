import functions
def main():
    while True:
        temp=input("Do you want to perform FFT? (Y/N) ")
        if temp=="N":
            filename=input("Enter your filename or STOP to quit ")
            if filename=="STOP":
                break
            functions.visualize(filename)
        elif temp=="Y":
            filename=input("Enter your filename or STOP to quit ")
            if filename=="STOP":
                break
            functions.all_fft(filename)
        else:
            print("Command not found.")
            continue
        
if __name__ == '__main__':
    main()