import folium
import pandas


class mapCreate:
    global mapID
    mapID = folium.Map(location=[38.58, -99.09],
                       zoom_start=6, tiles="stamen Terrain")

    def __init__(self):
        self.map = mapID
        self.fgv = ''
        self.fgp = ''
        self.txtFile = "Volcanoes.txt"
        self.jsonFile = "world.json"

    def changeColor(self, elevation):
        if elevation < 1000:
            return "green"
        elif 1000 <= elevation < 3000:
            return "orange"
        else:
            return "red"

    def addVolcanoes(self):
        self.fgv = folium.FeatureGroup(name="Volcanoes")

        data = pandas.read_csv(self.txtFile)

        html = """
            Volcano name:
            <br>
            <a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
            <br>
            Height: %s m
            """

        lat = list(data["LAT"])
        lon = list(data["LON"])
        elev = list(data["ELEV"])
        name = list(data["NAME"])

        for lt, ln, el, name in zip(lat, lon, elev, name):
            iframe = folium.IFrame(html=html % (
                name, name, str(el)), width=200, height=100)
            self.fgv.add_child(folium.Marker(location=[lt, ln],
                                             popup=folium.Popup(iframe), icon=folium.Icon(color=self.changeColor(el))))

    def addPopulation(self):
        self.fgp = folium.FeatureGroup(name="Population")

        self.fgp.add_child(folium.GeoJson(
            data=open(self.jsonFile, 'r', encoding='utf-8-sig').read(),
            style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                      else 'orange' if 10000000 < x['properties']['POP2005'] <= 20000000 else 'red'}))

    def addChild(self):
        self.map.add_child(self.fgv)
        self.map.add_child(self.fgp)

        self.map.add_child(folium.LayerControl())

    def saveMap(self):
        self.map.save("Map.html")


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
