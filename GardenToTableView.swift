import SwiftUI

struct GardenToTableView: View {
    var body: some View {
        NavigationStack {
            Text("Garden to Table")
                .font(.largeTitle)
                .navigationTitle("Garden to Table")
        }
    }
}

struct GardenToTableView_Previews: PreviewProvider {
    static var previews: some View {
        GardenToTableView()
    }
}
