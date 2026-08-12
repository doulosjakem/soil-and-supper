import SwiftUI

struct IdentifyView: View {
    var body: some View {
        NavigationStack {
            Text("Identify")
                .font(.largeTitle)
                .navigationTitle("Identify")
        }
    }
}

struct IdentifyView_Previews: PreviewProvider {
    static var previews: some View {
        IdentifyView()
    }
}
