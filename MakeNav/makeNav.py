# god this file is so hacky

from bs4 import BeautifulSoup
import argparse

coreScenes = ['Home Square', 'Game Space', 'Marketplace', 'Cinema', 'BasicApartment']

excludedScenes = ['DummyExclusionScene'] # Add scene names to this array to exclude them from the Navigator List.

parser = argparse.ArgumentParser()                                               

parser.add_argument("--scenelist", "-s", type=str, required=False)
parser.add_argument("--imageUrlRoot", "-i", type=str, required=False)
parser.add_argument("--addFunctions", "-f", type=int, required=False)
args = parser.parse_args()

def canReadData():
    try:
        with open(args.scenelist, 'r') as f:
            print("Scenelist opened!")
        print("Scenelist read success, hopefully! \n")
        return True
    except FileNotFoundError:
        print("No scenelist with the path/name of " + args.scenelist + " has been found. Aborting...")
        return False
    except:
        print("An unknown exception was thrown when trying to read the scenelist. Aborting...")
        return False


if args.scenelist == None:
   found = 0
   print("No scenelist specified! Will try to look within the working directory...")
   for potentialSceneListName in ['SCENELIST.XML', 'LOCALSCENELIST.XML', 'NAVSCENELIST.XML']:
       args.scenelist = potentialSceneListName
       if canReadData():
           print("While no scenelist was specified, a scenelist file was found in the working directory. This file will be used.")
           found = 1
           break
    
   if found == 0:
       args.scenelist = None
       print("Could not find a valid scenelist file in the working directory. Please ensure there is a file with the name of either SCENELIST.XML or LOCALSCENELIST.XML in your working directory.")
        

if args.imageUrlRoot == None:
    args.imageUrlRoot = "http://scea-home.playstation.net/a.home/mfe/content/"
    print("No Image URL Root found! Defaulting to SCEA Stock URL...")

if args.addFunctions == None:
    args.addFunctions = 0
elif args.addFunctions > 1 | args.addFunctions < 0:
    args.addFunctions = 0

def findAllScenes(parsedData):
    scenes = parsedData.find_all('SCENE')
    print(scenes)

def isThisSceneExcluded(sceneName):
    for exclusion in excludedScenes:
      if sceneName == exclusion:
        print(sceneName + ' has been specified as excluded. It will not appear in the navigator.')
        return True
    return False

def isThisACoreScene(sceneName):
    for core in coreScenes:
      if sceneName == core:
        return True
    return False

def getOtherSceneNames(parsedData):
    sceneNames = []
    for sceneName in parsedData.find_all('SCENE'):
        if not isThisACoreScene(sceneName.get('Name')):
            sceneNames.append(sceneName.get('Name'))
    return sceneNames

def getCoreSceneNames(parsedData):
    coreSceneNames = []
    for sceneName in parsedData.find_all('SCENE'):
        if isThisACoreScene(sceneName.get('Name')):
            coreSceneNames.append(sceneName.get('Name'))
    return coreSceneNames

def writeNavigatorStart(navFile):
    if navFile:
        nav.write('<XML>\n  <CONFIG>\n    <BGTYPE>GRAVPARTICLES</BGTYPE>\n  </CONFIG>\n')

def writeNavigatorCategoryStart(navFile, categoryName='Explore', categoryColor='#000000', categoryImage=args.imageUrlRoot+'Navigator/Main_Explorer1.dds'):
    if navFile:
        nav.write('  <CATEGORY BGCOLOR="'+categoryColor+'">\n')
        nav.write('    <TEXT LANG="en-GB">' + categoryName + '</TEXT>\n')
        nav.write('    <IMAGE LANG="en-GB">'+ categoryImage + '</IMAGE>\n')

def writeNavigatorCategoryEnd(navFile):
    if navFile:
        nav.write('  </CATEGORY>\n')

def writeNavigatorEntry(navFile, sceneName='BasicApartment'):
    if navFile:
        nav.write('    <ITEM>\n')
        nav.write('      <DESTINATION>' + sceneName + '</DESTINATION>\n')
        nav.write('    </ITEM>\n')

def writeNavigatorFunction(navFile, functionName, displayName='Untitled Function', imageURLSuffix='Navigator/Sub_RecentlyVisited_01.dds'):
    if navFile:
        nav.write('    <ITEM>\n')
        nav.write('      <TEXT LANG="en-GB">' + displayName + '</TEXT>\n')
        nav.write('      <IMAGE LANG="en-GB">' + args.imageUrlRoot + imageURLSuffix + '</IMAGE>\n')
        nav.write('      <FUNCTION>' + functionName + '</FUNCTION>\n')
        nav.write('    </ITEM>\n')

def writeNavigatorEnd(navFile):
    if navFile:
        nav.write('</XML>')

def writeNavigatorFile(parsedData, navFile):
    myCoreScenes = getCoreSceneNames(parsedData)
    myExploreScenes = getOtherSceneNames(parsedData)
    writeNavigatorStart(navFile)

    if args.addFunctions == 1:
        print("Adding functions category...")
        writeNavigatorCategoryStart(navFile, categoryName='My Home', categoryImage=args.imageUrlRoot+'Navigator/Main_MyHome_01.dds')
        writeNavigatorFunction(navFile, 'Favourites', 'Favorites', 'Navigator/Sub_MyFavorites_01.dds')
        writeNavigatorFunction(navFile, 'RecentlyVisited', 'Recently Visited')
        writeNavigatorCategoryEnd(nav)

    if len(myCoreScenes) > 0:
        print("Core scenes found!")
        writeNavigatorCategoryStart(navFile, categoryName='Core', categoryImage=args.imageUrlRoot+'Navigator/Main_CoreSpace_01.dds')
        for coreScene in myCoreScenes:
            if not isThisSceneExcluded(coreScene):
                writeNavigatorEntry(nav, coreScene)
        writeNavigatorCategoryEnd(nav)

    if len(myExploreScenes) > 0:
        print("Non-core scenes found!")
        writeNavigatorCategoryStart(navFile)
        for exploreScene in myExploreScenes:
            if not isThisSceneExcluded(exploreScene):
                writeNavigatorEntry(nav, exploreScene)
        writeNavigatorCategoryEnd(nav)

    writeNavigatorEnd(nav)
    

canRead = canReadData()
if canRead:
    with open(args.scenelist, 'r') as f:
            data = f.read()
    parsed_data = BeautifulSoup(data, "xml")
    nav = open('nav.xml', 'w')
    writeNavigatorFile(parsed_data, nav)
    nav.close()
    print("Done! Some work can be done on your end to pretty it up or add different categories, though!")
