import SwiftUI
import SwiftData

struct DesireDetailView: View {
    @Bindable var desire: Desire
    @Environment(\.modelContext) private var modelContext
    @State private var showingEdit = false

    var body: some View {
        Form {
            Section("Desire") {
                Text(desire.cropName)
                    .font(.headline)

                if let variety = desire.variety, !variety.isEmpty {
                    Text(variety)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }

                if let notes = desire.notes, !notes.isEmpty {
                    Text(notes)
                        .font(.body)
                } else {
                    Text("No notes")
                        .font(.body)
                        .foregroundStyle(.secondary)
                }
            }

            if !desire.isFulfilled && !desire.isCancelled && !desire.isExpired {
                Section {
                    Button("Mark fulfilled") {
                        GardenService.fulfillDesire(desire)
                    }
                    Button("Cancel", role: .destructive) {
                        GardenService.cancelDesire(desire)
                    }
                }
            }
        }
        .navigationTitle(desire.displayName)
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button("Edit") {
                    showingEdit = true
                }
            }
        }
        .sheet(isPresented: $showingEdit) {
            EditDesireView(desire: desire)
        }
    }
}

struct DesireDetailView_Previews: PreviewProvider {
    static var previews: some View {
        DesireDetailView(desire: Desire(cropName: "Carrots", variety: "Nantes"))
    }
}
