#from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import urllib2
import unicodedata
try:
   import cPickle as pickle
except:
   import pickle

myIngredients = ["Jameson Irish whiskey", "Mountain Dew Code Red soda", "gin", "dry vermouth", "sweet vermouth", "Malibu coconut rum",
                "Captain Morgan spiced rum", "rum", "lime juice", "Red Bull energy drink", "ice", "Jose Cuervo silver tequila",
                  "grenadine syrup", "orange juice", "Bacardi Superior rum", "club soda", "tequila"];

#  Ingredients with proper formatting
#Jameson Irish whiskey
#tequila
#Mountain Dew Code Red soda
#gin
#dry vermouth
#sweet vermouth
#vodka
#Southern Comfort peach liqueur
#Grand Marnier orange liqueur
#pineapple juice
#Malibu coconut rum
#Dr. Pepper soda
#Captain Morgan spiced rum
#apple juice
#ginger ale
#rum
#Chambord raspberry liqueur
#lime juice
#Red Bull energy drink
#ice
#Jose Cuervo silver tequila
#Jose Cuervo Especial gold tequila
#grenadine syrup
#orange juice
#pineapple juice
#Bacardi 151 rum
#Bacardi Superior rum
#club soda


f = open ('C://Users//Kevin//My Programming//workspace//Cock Tail Scraper//test.txt', 'rb')
#f = open('/home/kevin/workspace/textFiles/test.txt', 'rb') # to load

masterDict = 0;
try:
    masterDict = pickle.load(f)
except:   #does not exist, make empty dict
    print "except"
    f.close()
    f = open('/home/kevin/workspace/textFiles/test.txt', 'wb')## to dump
    pickle.dump({}, f)
    f.close()
    f = open('/home/kevin/workspace/textFiles/test.txt', 'rb') # to load
    masterDict = pickle.load(f)


masterList = []

i = 1
matchCounter = 0
listOfMatchingUrls = []
while i < 12317:#12318:
    url = "http://www.drinksmixer.com/drink" + str(i) + ".html"
    listOfMatchingUrls.append(url)

    #if i % 1000 == 0:# every 500 re write
     #   f.close();
      #  f = open('/home/kevin/workspace/textFiles/test.txt', 'wb')## to dump
       # pickle.dump(masterDict, f)
        #f.close()
        #f = open('/home/kevin/workspace/textFiles/test.txt', 'rb') # to load
        #masterDict = pickle.load(f)  
    if i in masterDict:
        result = masterDict[i]
        if result == "no url":   #found but had no url
            print "NO URL"
        else:
            masterList.append(masterDict[i])
    else:
        opener = urllib2.build_opener()
        try:
            url_opener = opener.open(url)
            page = url_opener.read()
            html = BeautifulSoup(page) 
            bySpan = html.find_all('span')
            ingredientsList = []
            for element in bySpan:
                myList = list(element.children)
                if len(myList) == 3:
                    newSpan = myList[2]
                    getATag = newSpan.find_all("a")
                    listOfChildren = list(getATag[0].children)
                    singleItem = listOfChildren[0].string
                    singleItemStripped = unicodedata.normalize('NFKD', singleItem).encode('ascii', 'ignore')
                    ingredientsList.append(singleItemStripped)
            masterList.append(ingredientsList);
            masterDict[i] = ingredientsList
        except:
            print "URL DID NOT EXIST"
            masterDict[i] = "no url"
    i = i + 1

### done cacheing

f.close();
f = open('C://Users//Kevin//My Programming//workspace//Cock Tail Scraper//test.txt', 'wb')## to dump
pickle.dump(masterDict, f)
f.close()

print "---------------------"
print "Possible Recipies:"

counter = -1;

for singleRecipe in masterList:
        
    counter = counter + 1;
         
    haveWholeRecipe = True;
    
    for singleNeededIngredient in singleRecipe:
        
        haveSingle = False
        
        for mySingleRecipe in myIngredients:
            if singleNeededIngredient == mySingleRecipe: #we have it
                haveSingle = True;
                break;
        if haveSingle == False: ## do not have an ingredient
            haveWholeRecipe = False;
            break
    if haveWholeRecipe == True and len(singleRecipe) != 0:
        print listOfMatchingUrls[counter]
        print singleRecipe

print "END"
