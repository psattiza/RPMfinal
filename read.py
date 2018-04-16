import csv

def readPreCoReq(filename):
    courses = []
    creditHours = {}
    prereqs = {}
    coreqs = {}
    try:
        f = open(filename)
        i=1
        reader = csv.reader(f)
        for line in reader:
            course = line[0]
            courses.append(course)
            try:
                numCredits = float(line[1])
                creditHours[course] = numCredits
                numPreReqs = int(line[2])
                if(numPreReqs !=0):
                    prereqs[course] = line[2+1:2+1+numPreReqs]
                numCoReqs = int(line[2+1+numPreReqs])
                if(numCoReqs !=0):
                    coreqs[course] = line[2+1+numPreReqs+1:2+1+numPreReqs+numCoReqs+1]
            except ValueError:
                print("Line #{} not formatted like [title,numCredits (float), numPrereqs,..., numCoReqs, ...] make sure you include zeros".format(line))
                return 0
            except IndexError:
                print("Line #{} not formatted like [title,numCredits (float), numPrereqs,..., numCoReqs, ...] make sure you include zeros".format(line))
                return 0
        return courses, creditHours, prereqs, coreqs
    except IOError:
        print("File: %s, not found" % filename)
   
def readCirriculum(filename):
    required = []
    electives = []
    try:
        f = open(filename)
        i=1
        reader = csv.reader(f)
        for line in reader:
            print line
            name = line[0]
            try:
                numRequired = int(line[1])
                numCredits = float(line[2])
                if((numRequired == -1) & (numCredits == -1)):
                    required = line[3:]
                else:
                    electives.append([name,numRequired, numCredits]+line[3:])
            except ValueError:
                print("Line #{} not formatted like [name,numrequired, numcredits...]".format(line))
                return 0
            except IndexError:
                print("Line #{} not formatted like [name,numrequired, numcredits...]".format(line))
                return 0
        return required, electives
    except IOError:
        print("File: %s, not found" % filename)
   

print readCirriculum("cirriculum.csv")
print readPreCoReq("constraints.csv")
