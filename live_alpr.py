from openalpr import Alpr
import csv, os, sys, threading

alpr = Alpr("us", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")

if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)

alpr.set_top_n(20)
alpr.set_default_region("in")

print("%-24s%-12s%-6s%-40s" % ("Image Name", "Plate", "Conf", "Details"))

def search_database(lpNumber):
        with open('database.csv') as database:
                reader = csv.DictReader(database)
                for row in reader:
                        if row['lp_number'].lower() == lpNumber.lower():
                                return row['LastName'] + ", " + row['FirstName'] + " " + row['Department']
                        else:
                                return ""
                        
def proccess_results(fileName, results):
        for plate in results['results']:
                for candidate in plate['candidates']:
                        resultStr = search_database(candidate['plate'])
                        if resultStr != "":
                                print("%-24s%-12s%-6.2f%-40s" % (fileName, candidate['plate'], candidate['confidence'], resultStr))
                                
                                
def proccess_images():
        for file in os.listdir("./images"):
                if file.endswith(".jpg"):
                        results = alpr.recognize_file("./images/" + file)
                        proccess_results(file, results)
                        os.rename("./images/" + file, "./images/completed/" + file)
        threading.Timer(1, proccess_images).start()
        
proccess_images()
