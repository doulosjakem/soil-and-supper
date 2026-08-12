import SwiftUI

struct HarvestView: View {
    var body: some View {
        NavigationStack {
            Text("Harvest")
                .font(.largeTitle)
                .navigationTitle("Harvest")
        }
    }
}

struct HarvestView_Previews: PreviewProvider {
    static var previews: some View {
        HarvestView()
    }
}
