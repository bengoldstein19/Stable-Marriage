import csv #import csv to read/write csv files
from random import shuffle #import shuffle to randomly order list

#DEFAULT VALUES FOR NAMES AND NUM NAMES
men_names = ["Andrew", "Benjamin", "Chris", "David", "Earl", "Frank", "George", "Harry", "Isaiah", "Jack", "Kyle", "Landry", "Mark", "Nick", "Oscar", "Phil", "Quinn", "Rob", "Steve", "Tim", "Ulysses", "Victor", "Walter", "Xavier", "Yosef", "Zach"]
women_names = ["Allie", "Bonnie", "Chloe", "Deandra", "Ella", "Felicia", "Gillian", "Holly", "Iris", "Jackie", "Kate", "Lynn", "Michelle", "Nicole", "Olivia", "Phyllis", "Queen", "Rashida", "Sydney", "Tilly", "Ursula", "Victoria", "Wendy", "Xia", "Yoko", "Zoe"]
N = 26

#INITIALIZE EMPTY GLOBALS FOR MEN AND WOMEN
men = []
women = []

#CLASS FOR MAN, HAS ATTRIBUTES RANKINGS, NAME, PROPOSED_TO, ENGAGED_TO, INDEX
class Man:
    def __init__(self, name, index):
        self.rankings = [] #array of indices of women in order of desirability to that man
        self.name = name #name of man
        self.proposed_to = [] #array of indices of women who that man has already proposed to
        self.engaged_to = N #index of woman that man is engaged to (default value number of names because out of bounds)
        self.list_index = index #index of that man in the men array

    def propose(self): #propose function
        if self.engaged_to == N: #if the man isn't engaged
            for woman_index in self.rankings: #for each women in the rankings starting with most desirable
                if not woman_index in self.proposed_to: #if you haven't proposed to her yet
                    women[woman_index].suitors.append(self.list_index) #add yourself to her list of suitors
                    self.proposed_to.append(woman_index) #add her to your list of proposed to women
                    return #terminate method

class Woman: #CLASS FOR WOMAN, HAS ATTRIVUTES RANKINGS, NAME, SUITORS, ENGAGED_TO, INDEX
    def __init__(self, name, index):
        self.rankings = [] #array of indices of men in order of desirability to that woman
        self.name = name #name of woman
        self.suitors = [] #array of indices of men currently proposing to that women
        self.engaged_to = N #index of man that woman is engaged to (default value number of names because out of bounds)
        self.list_index = index #index of that woman in the women array

    def pick_a_suitor(self): #pick a suitor function (in response to proposal)
        for man_index in self.rankings: #for each man in order of desirability
            if man_index == self.engaged_to: #if you're engaged to that man
                self.suitors = [] #reset suitors
                return #terminate method (no need to make a change)
            for suitor_index in self.suitors: #for each suitor
                if suitor_index == man_index: #if the suitor is the man you're currently on the rankings
                    if not self.engaged_to == N: #if you're already engaged
                        men[self.engaged_to].engaged_to = N #dump the guy you're engaged to (set his engaged_to to N)
                    self.engaged_to = suitor_index #set you're engaged_to to the suitor
                    men[suitor_index].engaged_to = self.list_index #set the suitors engaged_to to your index
                    self.suitors = [] #reset suitors
                    return #temrinate method
        self.suitors = [] #if you reach the end reset suitors anyway

#MAIN FUNCTION (ACTUALLY RUN)
def main():
    yn = input("Use files? (y/n) ") #get string input
    if yn == "y": #if you want to use files
        get_marriages_file() #get the marriages from file
    elif yn == "n": #if you don't want to use the files
        get_marriages_random() #use randomly generated from defaults
    else: #otherwise
        main() #restart and get input again

#GET MARRIAGES FROM FILE FUNCTION
def get_marriages_file():
    global N #make N refer to global variable instead of create new local
    get_names() #fill names array with file values
    N = len(men_names) #set number of names to number of names in file
    i=0 #set counter for index of men
    for man_name in men_names: #for each name in the man name array
        men.append(Man(man_name, i)) #add a new man with the appropriate name and index to the array
        i+=1 #increment counter
    i=0 #reset counter for the women
    for woman_name in women_names: #for each name in the woman name array
        women.append(Woman(woman_name,i)) #add a new woman with the appropriate name and index to the array
        i+=1 #increment counter
    get_men_rankings() #get appropriate rankings for each man from file
    get_women_rankings() #get appropriate rankings for each woman from file
    while some_unengaged(): #while there still are people not engaged
        for man in men: #for each man
            man.propose() #have that man propose to his favorite
        for woman in women: #for each woman
            woman.pick_a_suitor() #have that woman pick a suitor from the men who proposed to her
    print_marriages() #after everyone engaged print marriages

#GET MARRIAGES FROM DEFAULT LISTS AND RANDOM RANKINGS
def get_marriages_random():
    i=0 #set counter for index of men
    for man_name in men_names: #for each name in the man name array
        men.append(Man(man_name, i)) #add a new man with the appropriate name and index to the array
        i+=1 #increment counter
    i=0 #reset counter for the women
    for woman_name in women_names: #for each name in the woman name array
        women.append(Woman(woman_name,i)) #add a new woman with the appropriate name and index to the array
        i+=1 #increment counter
    for man in men: #for each man
        man.rankings = list(range(26)) #make the man's rankings in order
        shuffle(man.rankings) #shuffle em up
    for woman in women: #for each woman
        woman.rankings = list(range(26)) #make the woman's rankings in order
        shuffle(woman.rankings) #shuffle em up
    while some_unengaged(): #while there are still some not engaged
        for man in men: #for each man
            man.propose() #have them propose to their favorite woman
        for woman in women: #for each woman
            woman.pick_a_suitor() #have that woman pick a suitor from the men who proposed to her
    print_marriages() #after everyone engaged print marriages
    write_out_rankings() #write rankings to outfiles

#GET NAMES FROM FILE FUNCTION
def get_names():
    global men_names #make men_names and women_names refer to globals instead of creating new locals with same name
    global women_names
    men_names = [] #reset men_names and women_names (erase default vals)
    women_names = []
    with open("men_rankings.csv") as men_rankings: #open men ranking file
        reader = csv.reader(men_rankings) #create reader object for men_rankings file
        for line in reader: #for each line in the reader
            for element in line: #for each element in the line
                men_names.append(element) #add the element to the men_names array
            break #break so this is only done for the first line
    with open("women_rankings.csv") as women_rankings: #open women ranking file
        reader = csv.reader(women_rankings) #create reader object for women ranking file
        for line in reader: #for each line in the reader
            for element in line: #for each element in the line
                women_names.append(element) #append element to the women_names array
            break #break so this is only done for first line

#GET MEN RANKINGS FROM FILE
def get_men_rankings():
    with open("men_rankings.csv") as men_rankings: #open men rankings file
        reader = csv.reader(men_rankings) #create reader object for men rankings file
        not_first_line = False #create bool to store whether line is header (first) line
        for line in reader: #for each line
            if not_first_line: #if line is not header (not first line)
                for j in range(N): #for each element in the line (jth element)
                    men[j].rankings.append(women_names.index(line[j])) #add that element to the jth man's ranking list
            else:
                not_first_line = True #after first line set not_first_line to true

#GET WOMEN RANKINGS FROM FILE
def get_women_rankings():
    with open("women_rankings.csv") as women_rankings: #open women ranking file
        reader = csv.reader(women_rankings) #make reader object for women rankings file
        not_first_line = False #create bool to store whether line is header (first) line
        for line in reader: #for each line in reader
            if not_first_line: #if not the first line
                for j in range(N): #for each element of the line (jth element)
                    women[j].rankings.append(men_names.index(line[j])) #add element to jth woman's ranking list
            else:
                not_first_line = True #after first line set not_first_line to true

#TELL IF THERE ARE STILL SOME UNENGAGED LEFT
def some_unengaged():
    for woman in women: #for each woman
        if woman.engaged_to == N: #if woman has default engaged_to value
            return True #return true because that woman is unengaged
    return False #if no woman unengaged (True hasn't been returned) return false

#PRINT ALL MARRIAGES
def print_marriages():
    for man in men: #FOR EACH MAN
        print(f"{man.name} is married to {women[man.engaged_to].name}, his choice #{man.rankings.index(women[man.engaged_to].list_index) + 1} and her choice #{women[man.engaged_to].rankings.index(man.list_index) + 1}") #print names and rankings of the married couple

#WRITE RANKINGS TO OUTFILE
def write_out_rankings():
    with open("random_men_rankings.csv", "w") as random_men_rankings: #create csv file for men's rankings
        writer = csv.writer(random_men_rankings) #create writer object for the file
        writer.writerow(men_names) #write the men's names at the top
        for i in range(N): #for each row i
            writer.writerow([women[man.rankings[i]].name for man in men]) #write out the ith rankings of the man in matching column
    with open("random_women_rankings.csv", "w") as random_women_rankings: #create csv file for women's rankings
        writer = csv.writer(random_women_rankings) #create writer object for the file
        writer.writerow(women_names) #write the women's names at the top
        for i in range(N): #for each row i
            writer.writerow([men[woman.rankings[i]].name for woman in women]) #write out the ith rankings of the woman in the matching column

main() #run main function
