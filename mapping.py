import folium
import pandas

class mapCreate:
    # global function to define a location where the map is started with and a zoom size and a map format 
    global mapID
    mapID = folium.Map(location=[38.58, -99.09],
                       zoom_start=6, tiles="stamen Terrain")
    
    # initialize mapID as a self.map 
    def __init__(self):
        self.map = mapID
        self.fgv = ''
        self.fgp = ''
        self.txtFile = "Volcanoes.txt"
        self.jsonFile = "world.json"
    
    # return a different color depended on the height of volcanoes
    def changeColor(self, elevation):
        if elevation < 1000:
            return "green"
        elif 1000 <= elevation < 3000:
            return "orange"
        else:
            return "red"
    
    # add markers pointing to a location of volcanoes and having some description
    def addVolcanoes(self):
        # initialize fgv to design map based on this 
        self.fgv = folium.FeatureGroup(name="Volcanoes")
        
        # read a file through pandas 
        data = pandas.read_csv(self.txtFile)
        
        # used this html for description inside of marker 
        html = """
            Volcano name:
            <br>
            <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
            <br>
            Height: %s m
            """
        
        # initialize each values as a list from the data scaned by pandas 
        lat = list(data["LAT"])
        lon = list(data["LON"])
        elev = list(data["ELEV"])
        name = list(data["NAME"])
        
        # used for-loop to pass all data 
        # zip() can store multiple lists as one 
        for lt, ln, el, name in zip(lat, lon, elev, name):
            # dsign popup box from marker 
            iframe = folium.IFrame(html=html % (
                name, name, str(el)), width=200, height=100)
            self.fgv.add_child(folium.Marker(location=[lt, ln],
                                             popup=folium.Popup(iframe), icon=folium.Icon(color=self.changeColor(el))))
    
    # change to a monopolical map and distinguish a color with population 
    def addPopulation(self):
        self.fgp = folium.FeatureGroup(name="Population")
        
        # use GeoJson to open and read a json file 
        self.fgp.add_child(folium.GeoJson(
            data=open(self.jsonFile, 'r', encoding='utf-8-sig').read(),
            style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                      else 'orange' if 10000000 < x['properties']['POP2005'] <= 20000000 else 'red'}))
    
    # finalize all childs based on the first map initialization 
    def addChild(self):
        self.map.add_child(self.fgv)
        self.map.add_child(self.fgp)
        
        # Be able to switch on and off for the two added childs
        self.map.add_child(folium.LayerControl())
       
    # save every changes to html files in the same folder 
    def saveMap(self):
        self.map.save("Map.html")

# create another class to simplify the main function 
class mainMenu:
    def __init__(self):
        self.main = mapCreate()

    def activateMap(self):
        self.main.addVolcanoes()
        self.main.addPopulation()
        self.main.addChild()
        self.main.saveMap()


def main():

    key = mainMenu()
    key.activateMap()


if __name__ == '__main__':
    main()
