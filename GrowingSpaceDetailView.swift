import SwiftUI
import SwiftData

struct GrowingSpaceDetailView: View {
    @Bindable var space: GrowingSpace
    @Environment(\.modelContext) private var modelContext
    @State private var showingEdit = false
    @State private var showingRecordPlanting = false

    private var activeOccupancies: [Occupancy] {
        space.occupancies
            .filter { $0.status == .active }
            .sorted { $0.startDate > $1.startDate }
    }

    private var pastOccupancies: [Occupancy] {
        space.occupancies
            .filter { $0.status != .active }
            .sorted { $0.startDate > $1.startDate }
    }

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

            if activeOccupancies.isEmpty {
                Section("Current") {
                    ContentUnavailableView {
                        Label("Nothing growing here yet", systemImage: "leaf")
                    } actions: {
                        Button("Plant something") {
                            showingRecordPlanting = true
                        }
                    }
                }
            } else {
                Section("Currently growing") {
                    ForEach(activeOccupancies) { occupancy in
                        VStack(alignment: .leading, spacing: 4) {
                            Text(occupancy.displayName)
                                .font(.headline)
                            Text(occupancy.startDate, format: .dateTime.day().month().year())
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }

                Section {
                    Button("Mark as finished") {
                        for occupancy in activeOccupancies {
                            GardenService.completeOccupancy(occupancy)
                        }
                    }
                }
            }

            if !pastOccupancies.isEmpty {
                Section("History") {
                    ForEach(pastOccupancies) { occupancy in
                        VStack(alignment: .leading, spacing: 4) {
                            Text(occupancy.displayName)
                                .font(.headline)
                            Text(dateRangeString(for: occupancy))
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }
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
                    GardenService.deleteGrowingSpace(space, in: modelContext)
                }
            }
        }
        .sheet(isPresented: $showingEdit) {
            AddEditGrowingSpaceView(space: space)
        }
        .sheet(isPresented: $showingRecordPlanting) {
            RecordPlantingView(growingSpace: space)
        }
    }

    private func dateRangeString(for occupancy: Occupancy) -> String {
        let start = occupancy.startDate.formatted(date: .abbreviated, time: .omitted)
        if let end = occupancy.endDate {
            return "\(start) – \(end.formatted(date: .abbreviated, time: .omitted))"
        }
        return start
    }
}

struct GrowingSpaceDetailView_Previews: PreviewProvider {
    static var previews: some View {
        GrowingSpaceDetailView(space: GrowingSpace(name: "Bed 1"))
    }
}
