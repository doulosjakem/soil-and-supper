import SwiftUI

struct GardenView: View {
    var body: some View {
        NavigationStack {
            Text("Garden")
                .font(.largeTitle)
                .navigationTitle("Garden")
        }
    }
}

struct GardenView_Previews: PreviewProvider {
    static var previews: some View {
        GardenView()
    }
}
