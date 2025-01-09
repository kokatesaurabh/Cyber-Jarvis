import webbrowser

def osint_tool():
    while True:
        print("\nOSINT Options:")
        print("1. OSINT Framework - https://osintframework.com/")
        print("2. Link Extractor - https://www.webtoolhub.com/tn561364-link-extractor.aspx")
        print("3. DNS Lookup - https://www.nslookup.io/domains/karolinaprotsenko.com/dns-records/")
        print("4. Wayback Machine - https://web.archive.org/web/20240000000000*/https://karolinaprotsenko.com/")
        print("5. Image Search:")
        print("   a. Exif Data - https://jimpl.com/")
        print("   b. Reverse Image Lookup - https://www.duplichecker.com/reverse-image-search.php")
        print("6. Facial Recognition - https://pimeyes.com/en")
        print("7. Search Internal Information of Websites - https://search.censys.io/")

        option = input("\nEnter your choice (or type 'exit' to quit): ")

        if option == "1":
            webbrowser.open("https://osintframework.com/")
        elif option == "2":
            webbrowser.open("https://www.webtoolhub.com/tn561364-link-extractor.aspx")
        elif option == "3":
            webbrowser.open("https://www.nslookup.io/domains/karolinaprotsenko.com/dns-records/")
        elif option == "4":
            webbrowser.open("https://web.archive.org/web/20240000000000*/https://karolinaprotsenko.com/")
        elif option == "5":
            image_option = input("Select an image search option (a or b): ")
            if image_option == "a":
                webbrowser.open("https://jimpl.com/")
            elif image_option == "b":
                webbrowser.open("https://www.duplichecker.com/reverse-image-search.php")
            else:
                print("Invalid option!")
        elif option == "6":
            webbrowser.open("https://pimeyes.com/en")
        elif option == "7":
            webbrowser.open("https://search.censys.io/")
        elif option.lower() == "exit":
            print("Exiting the OSINT tool. Goodbye!")
            break
        else:
            print("Invalid option! Please try again.")

# Uncomment the following line if you want to execute the function when running the script directly
# osint_tool()
