# MakeNav
MakeNav is a python script aimed at Python 3 for the purpose of creating Navigator XML files for PlayStation Home.

## Dependencies
You will need the following:
- Python 3.10 or higher
- BeautifulSoup4 (pip install BeautifulSoup4)
- lxml (pip install lxml)
- A SCENELIST.XML or LOCALSCENELIST.XML file to parse
- Some knowledge on how to use a command line program

## Usage
(WIP)

Sample: "makeNav.py -s path/to/scenelist.xml"

If it succeeded, you should see nav.xml in the working directory.

## Am I done just like that?
I'd say you'd still have a bit of work to do -- primarily in changing the image urls as they are still pointing to Sony's defunct servers. However, you can also tidy up your newfound navigator file by adding more categories and the like.
