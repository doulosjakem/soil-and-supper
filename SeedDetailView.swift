import SwiftUI
import SwiftData

struct SeedDetailView: View {
    @Bindable var seed: Seed
    @Environment(\.modelContext) private var modelContext
    @State private var showingEdit = false

    var body: some View {
        Form {
            Section("Seed Info") {
                TextField("Crop Name", text: $seed.cropName)
                TextField("Variety", text: $seed.variety ?? "")
                Picker("State", selection: $seed.state) {
                    ForEach(SeedState.allCases, id: \.self) { state in
                        Text(state.displayName).tag(state)
                    }
                }
                TextField("Notes", text: $seed.notes ?? "", axis: .vertical)
                    .lineLimit(3...6)
            }
        }
        .navigationTitle(seed.cropName)
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button("Edit") {
                    showingEdit = true
                }
            }
            ToolbarItem(placement: .destructiveAction) {
                Button("Delete", role: .destructive) {
                    modelContext.delete(seed)
                }
            }
        }
        .sheet(isPresented: $showingEdit) {
            AddEditSeedView(seed: seed)
        }
    }
}

struct SeedDetailView_Previews: PreviewProvider {
    static var previews: some View {
        SeedDetailView(seed: Seed(cropName: "Carrot", variety: "Nantes", state: .own))
    }
}
