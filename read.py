import csv

def readPreCoReq(filename):
    courses = []
    creditHours = {}
    prereqs = {}
    coreqs = {}
    try:
        with open(filename) as f:
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
        with open(filename) as f:
            i=1
            reader = csv.reader(f)
            for line in reader:
                #print line
                name = line[0]
                try:
                    numRequired = int(line[1])
                    numCredits = float(line[2])
                    if((numRequired == -1) & (numCredits == -1)):
                        required = line[3:]
                    else:
                        electives.append([numRequired, numCredits]+line[3:])
                except ValueError:
                    print("Line #{} not formatted like [name,numrequired, numcredits...]".format(line))
                    return 0
                except IndexError:
                    print("Line #{} not formatted like [name,numrequired, numcredits...]".format(line))
                    return 0
            return required, electives
    except IOError:
        print("File: %s, not found" % filename)

def readSchedule(filename):
    fall = []#
    valid_falls = []#
    spring = []#
    valid_springs = []#
    other = {}#
    map_semester_to_number = {}#
    try:
        with open(filename) as f:
            reader = csv.reader(f)
            semesters = next(reader)
            for i, sem in enumerate(semesters):
                map_semester_to_number[sem] = i
                if sem.lower().startswith("s"):
                    valid_springs.append(i)
                elif sem.lower().startswith("f"):
                    valid_falls.append(i)


            for line in reader:
                course = line[0]
                if line[1].lower() == "a":
                    continue
                elif line[1].lower() == "f":
                    fall.append(course)
                elif line[1].lower() == "s":
                    spring.append(course)
                else:
                    sems = line[1].split()
                    other[course] = sems

            return fall, valid_falls, spring, valid_springs, other, map_semester_to_number
    except IOError:
        print("File: %s, not found" % filename)

def readTaken(filename):
    try:
        with open(filename) as f:
            reader = csv.reader(f)
            return next(reader)
    except IOError:
        print("File: %s, not found" % filename)


if __name__ == '__main__':
    #fall, valid_falls, spring, valid_springs, other, map_semester_to_number  = readSchedule("schedule.csv")
    #print("Fall: {}".format(fall))
    #print("Other: {}".format(other))
    #print(readCirriculum("cirriculum.csv"))
	#print(readPreCoReq("constraints.csv"))
	print(readTaken("taken.csv"))
