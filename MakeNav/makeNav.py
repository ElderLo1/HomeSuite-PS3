from bs4 import BeautifulSoup
import argparse

coreScenes = ['Home Square', 'Game Space', 'Marketplace', 'Cinema', 'BasicApartment']

parser = argparse.ArgumentParser()                                               

parser.add_argument("--scenelist", "-s", type=str, required=True)
args = parser.parse_args()
print("Attempting to open " + args.scenelist + "...")

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

def findAllScenes(parsedData):
    scenes = parsedData.find_all('SCENE')
    print(scenes)

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
        nav.write('<XML>\n  <CONFIG>\n    <BGTYPE>GRAVPARTICLES</BGTYPE>\n  <CONFIG>\n')

def writeNavigatorCategoryStart(navFile, categoryName='Explore', categoryColor='#000000', categoryImage='http://scea-home.playstation.net/a.home/mfe/content/Navigator/Main_Explorer1.dds'):
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


def writeNavigatorEnd(navFile):
    if navFile:
        nav.write('</XML>')

def writeNavigatorFile(parsedData, navFile):
    myCoreScenes = getCoreSceneNames(parsedData)
    myExploreScenes = getOtherSceneNames(parsedData)
    writeNavigatorStart(navFile)
    if len(myCoreScenes) > 0:
        print("Core scenes found!")
        writeNavigatorCategoryStart(navFile, categoryName='Core', categoryImage='http://scea-home.playstation.net/a.home/mfe/content/Navigator/Main_CoreSpace_01.dds')
        for coreScene in myCoreScenes:
            writeNavigatorEntry(nav, coreScene)
        writeNavigatorCategoryEnd(nav)

    if len(myExploreScenes) > 0:
        print("Non-core scenes found!")
        writeNavigatorCategoryStart(navFile)
        for exploreScene in myExploreScenes:
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
