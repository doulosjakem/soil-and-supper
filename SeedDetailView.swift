import SwiftUI
import SwiftData

struct SeedDetailView: View {
    @Bindable var seed: Seed
    @Environment(\.modelContext) private var modelContext
    @State private var showingEdit = false
    @State private var showingChangeState = false

    var body: some View {
        Form {
            Section("Seed Info") {
                Text(seed.cropName)
                    .font(.headline)

                if let variety = seed.variety, !variety.isEmpty {
                    Text(variety)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }

                HStack {
                    Text("State")
                    Spacer()
                    HStack(spacing: 6) {
                        Image(systemName: seed.state.symbolName)
                        Text(seed.state.displayName)
                    }
                    .foregroundStyle(.secondary)
                }

                if let notes = seed.notes, !notes.isEmpty {
                    Text(notes)
                        .font(.body)
                } else {
                    Text("No notes")
                        .font(.body)
                        .foregroundStyle(.secondary)
                }
            }
        }
        .navigationTitle(seed.displayName)
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Menu {
                    Button {
                        showingEdit = true
                    } label: {
                        Label("Edit", systemImage: "pencil")
                    }

                    Button {
                        showingChangeState = true
                    } label: {
                        Label("Change State", systemImage: "arrow.triangle.2.circlepath")
                    }
                } label: {
                    Label("Edit", systemImage: "pencil")
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
        .confirmationDialog("Change State", isPresented: $showingChangeState) {
            ForEach(SeedState.allCases, id: \.self) { state in
                Button(state.displayName) {
                    GardenService.changeSeedState(seed, to: state)
                }
            }
        }
    }
}

struct SeedDetailView_Previews: PreviewProvider {
    static var previews: some View {
        SeedDetailView(seed: Seed(cropName: "Carrot", variety: "Nantes", state: .own))
    }
}
