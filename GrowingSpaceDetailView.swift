import SwiftUI
import SwiftData

struct GrowingSpaceDetailView: View {
    @Bindable var space: GrowingSpace
    @Environment(\.modelContext) private var modelContext
    @State private var showingEdit = false

    var body: some View {
        Form {
            Section("Details") {
                Text(space.name)
                    .font(.headline)
                if let notes = space.notes, !notes.isEmpty {
                    Text(notes)
                        .font(.body)
                } else {
                    Text("No notes")
                        .font(.body)
                        .foregroundStyle(.secondary)
                }
            }

            Section("Current") {
                ContentUnavailableView(
                    "Nothing planted yet.",
                    systemImage: "leaf",
                    description: Text("Occupancy and planning features are coming soon.")
                )
            }
        }
        .navigationTitle(space.name)
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button("Edit") {
                    showingEdit = true
                }
            }
            ToolbarItem(placement: .destructiveAction) {
                Button("Delete", role: .destructive) {
                    modelContext.delete(space)
                }
            }
        }
        .sheet(isPresented: $showingEdit) {
            AddEditGrowingSpaceView(space: space)
        }
    }
}

struct GrowingSpaceDetailView_Previews: PreviewProvider {
    static var previews: some View {
        GrowingSpaceDetailView(space: GrowingSpace(name: "Bed 1"))
    }
}
