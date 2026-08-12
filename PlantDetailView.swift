import SwiftUI
import SwiftData

struct PlantDetailView: View {
    @Bindable var plant: Plant
    @Environment(\.modelContext) private var modelContext

    var body: some View {
        Form {
            Section("Details") {
                TextField("Name", text: $plant.name)
                TextField("Variety", text: $plant.variety ?? "")
                DatePicker("Planting Date", selection: Binding(
                    get: { plant.plantingDate ?? Date() },
                    set: { plant.plantingDate = $0 }
                ), displayedComponents: .date)
                TextField("Location", text: $plant.location ?? "")
            }

            Section("Notes") {
                TextField("Notes", text: $plant.notes ?? "", axis: .vertical)
                    .lineLimit(3...6)
            }
        }
        .navigationTitle(plant.name)
        .toolbar {
            ToolbarItem(placement: .destructiveAction) {
                Button("Delete") {
                    modelContext.delete(plant)
                }
            }
        }
        .onDisappear {
            plant.updatedAt = Date()
        }
    }
}

struct PlantDetailView_Previews: PreviewProvider {
    static var previews: some View {
        PlantDetailView(plant: Plant(name: "Tomato"))
    }
}
