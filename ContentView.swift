import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            GardenView()
                .tabItem {
                    Label("Garden", systemImage: "leaf")
                }

            HarvestView()
                .tabItem {
                    Label("Harvest", systemImage: "basket")
                }

            IdentifyView()
                .tabItem {
                    Label("Identify", systemImage: "camera")
                }

            GardenToTableView()
                .tabItem {
                    Label("Garden to Table", systemImage: "fork.knife")
                }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
