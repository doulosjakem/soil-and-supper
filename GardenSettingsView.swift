import SwiftUI
import SwiftData

struct GardenSettingsView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss
    @Query private var gardens: [Garden]

    @State private var name: String
    @State private var location: String
    @State private var climateZone: String
    @State private var lastFrostDate: Date
    @State private var firstFrostDate: Date

    init() {
        _name = State(initialValue: "")
        _location = State(initialValue: "")
        _climateZone = State(initialValue: "")
        _lastFrostDate = State(initialValue: Calendar.current.date(byAdding: .month, value: -6, to: Date()) ?? Date())
        _firstFrostDate = State(initialValue: Calendar.current.date(byAdding: .month, value: 6, to: Date()) ?? Date())
    }

    var existingGarden: Garden? {
        gardens.first
    }

    var body: some View {
        Form {
            Section("Garden") {
                TextField("Name", text: $name)
                TextField("Location", text: $location)
            }

            Section("Climate") {
                TextField("Climate Zone", text: $climateZone)
                DatePicker("Average Last Frost", selection: $lastFrostDate, displayedComponents: .date)
                DatePicker("Average First Frost", selection: $firstFrostDate, displayedComponents: .date)
            }
        }
        .navigationTitle("Garden Settings")
        .toolbar {
            ToolbarItem(placement: .cancellationAction) {
                Button("Cancel") {
                    dismiss()
                }
            }
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    saveSettings()
                }
            }
        }
        .onAppear {
            if let garden = existingGarden {
                name = garden.name
                location = garden.location ?? ""
                climateZone = garden.climateZone ?? ""
                lastFrostDate = garden.averageLastFrostDate ?? Calendar.current.date(byAdding: .month, value: -6, to: Date()) ?? Date()
                firstFrostDate = garden.averageFirstFrostDate ?? Calendar.current.date(byAdding: .month, value: 6, to: Date()) ?? Date()
            } else {
                name = "My Garden"
                location = ""
                climateZone = ""
                lastFrostDate = Calendar.current.date(byAdding: .month, value: -6, to: Date()) ?? Date()
                firstFrostDate = Calendar.current.date(byAdding: .month, value: 6, to: Date()) ?? Date()
            }
        }
    }

    private func saveSettings() {
        let trimmedName = name.trimmingCharacters(in: .whitespaces)
        guard !trimmedName.isEmpty else { return }

        let trimmedLocation = location.trimmingCharacters(in: .whitespaces)
        let trimmedClimateZone = climateZone.trimmingCharacters(in: .whitespaces)

        if let garden = existingGarden {
            garden.name = trimmedName
            garden.location = trimmedLocation.isEmpty ? nil : trimmedLocation
            garden.climateZone = trimmedClimateZone.isEmpty ? nil : trimmedClimateZone
            garden.averageLastFrostDate = lastFrostDate
            garden.averageFirstFrostDate = firstFrostDate
            garden.updatedAt = Date()
        } else {
            let newGarden = Garden(name: trimmedName, location: trimmedLocation.isEmpty ? nil : trimmedLocation)
            newGarden.climateZone = trimmedClimateZone.isEmpty ? nil : trimmedClimateZone
            newGarden.averageLastFrostDate = lastFrostDate
            newGarden.averageFirstFrostDate = firstFrostDate
            modelContext.insert(newGarden)
        }

        dismiss()
    }
}

struct GardenSettingsView_Previews: PreviewProvider {
    static var previews: some View {
        GardenSettingsView()
    }
}
