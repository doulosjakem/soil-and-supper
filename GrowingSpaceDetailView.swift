import SwiftUI
import SwiftData

struct GrowingSpaceDetailView: View {
    @Bindable var space: GrowingSpace
    @Environment(\.modelContext) private var modelContext
    @Query private var seeds: [Seed]
    @Query private var desires: [Desire]
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

    private var garden: Garden? {
        space.garden
    }

    private var suggestions: [PlantingSuggestion] {
        guard let garden else { return [] }
        let engine = DefaultPlanningEngine()
        return engine.suggestions(
            for: space,
            on: Date(),
            in: garden,
            seeds: seeds,
            desires: desires
        )
    }

    private var bestFitSuggestions: [PlantingSuggestion] {
        suggestions.filter { $0.ranking == .bestFit }
    }

    private var alsoGoodSuggestions: [PlantingSuggestion] {
        suggestions.filter { $0.ranking == .alsoGood }
    }

    private var futureSuggestions: [PlantingSuggestion] {
        guard let garden,
              let expectedRelease = activeOccupancies.compactMap(\.expectedReleaseDate).first else {
            return []
        }
        let engine = DefaultPlanningEngine()
        return engine.suggestionsForFutureOpening(
            of: space,
            openingDate: expectedRelease,
            in: garden,
            seeds: seeds,
            desires: desires
        )
    }

    private var futureBestFit: [PlantingSuggestion] {
        futureSuggestions.filter { $0.ranking == .bestFit }
    }

    private var futureAlsoGood: [PlantingSuggestion] {
        futureSuggestions.filter { $0.ranking == .alsoGood }
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

                if !suggestions.isEmpty {
                    Section("Suggestions") {
                        if !bestFitSuggestions.isEmpty {
                            ForEach(bestFitSuggestions) { suggestion in
                                VStack(alignment: .leading, spacing: 4) {
                                    HStack {
                                        Text(suggestion.cropName)
                                            .font(.headline)
                                        if let variety = suggestion.varietyName, !variety.isEmpty {
                                            Text(variety)
                                                .font(.subheadline)
                                                .foregroundStyle(.secondary)
                                        }
                                        Spacer()
                                        Text("Best fit")
                                            .font(.caption)
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 4)
                                            .background(.green.opacity(0.2))
                                            .foregroundStyle(.green)
                                            .clipShape(Capsule())
                                    }
                                    Text(suggestion.reason)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                    if let harvest = suggestion.estimatedHarvestDate {
                                        Text("Estimated harvest: \(harvest, format: .dateTime.day().month().year())")
                                            .font(.caption)
                                            .foregroundStyle(.secondary)
                                    }
                                }
                            }
                        }

                        if !alsoGoodSuggestions.isEmpty {
                            ForEach(alsoGoodSuggestions) { suggestion in
                                VStack(alignment: .leading, spacing: 4) {
                                    HStack {
                                        Text(suggestion.cropName)
                                            .font(.headline)
                                        if let variety = suggestion.varietyName, !variety.isEmpty {
                                            Text(variety)
                                                .font(.subheadline)
                                                .foregroundStyle(.secondary)
                                        }
                                        Spacer()
                                        Text("Also good")
                                            .font(.caption)
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 4)
                                            .background(.blue.opacity(0.2))
                                            .foregroundStyle(.blue)
                                            .clipShape(Capsule())
                                    }
                                    Text(suggestion.reason)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                    if let harvest = suggestion.estimatedHarvestDate {
                                        Text("Estimated harvest: \(harvest, format: .dateTime.day().month().year())")
                                            .font(.caption)
                                            .foregroundStyle(.secondary)
                                    }
                                }
                            }
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

                if let expectedRelease = activeOccupancies.compactMap(\.expectedReleaseDate).first {
                    Section {
                        HStack {
                            Image(systemName: "clock.arrow.circlepath")
                            Text("Expected opening ~\(expectedRelease, format: .dateTime.day().month().year())")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }
                }

                if !futureSuggestions.isEmpty {
                    Section("Next") {
                        if !futureBestFit.isEmpty {
                            ForEach(futureBestFit) { suggestion in
                                VStack(alignment: .leading, spacing: 4) {
                                    HStack {
                                        Text(suggestion.cropName)
                                            .font(.headline)
                                        if let variety = suggestion.varietyName, !variety.isEmpty {
                                            Text(variety)
                                                .font(.subheadline)
                                                .foregroundStyle(.secondary)
                                        }
                                        Spacer()
                                        Text("Best fit")
                                            .font(.caption)
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 4)
                                            .background(.green.opacity(0.2))
                                            .foregroundStyle(.green)
                                            .clipShape(Capsule())
                                    }
                                    Text(suggestion.reason)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                    if let harvest = suggestion.estimatedHarvestDate {
                                        Text("Estimated harvest: \(harvest, format: .dateTime.day().month().year())")
                                            .font(.caption)
                                            .foregroundStyle(.secondary)
                                    }
                                }
                            }
                        }

                        if !futureAlsoGood.isEmpty {
                            ForEach(futureAlsoGood) { suggestion in
                                VStack(alignment: .leading, spacing: 4) {
                                    HStack {
                                        Text(suggestion.cropName)
                                            .font(.headline)
                                        if let variety = suggestion.varietyName, !variety.isEmpty {
                                            Text(variety)
                                                .font(.subheadline)
                                                .foregroundStyle(.secondary)
                                        }
                                        Spacer()
                                        Text("Also good")
                                            .font(.caption)
                                            .padding(.horizontal, 8)
                                            .padding(.vertical, 4)
                                            .background(.blue.opacity(0.2))
                                            .foregroundStyle(.blue)
                                            .clipShape(Capsule())
                                    }
                                    Text(suggestion.reason)
                                        .font(.caption)
                                        .foregroundStyle(.secondary)
                                    if let harvest = suggestion.estimatedHarvestDate {
                                        Text("Estimated harvest: \(harvest, format: .dateTime.day().month().year())")
                                            .font(.caption)
                                            .foregroundStyle(.secondary)
                                    }
                                }
                            }
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
            .modelContainer(for: [GrowingSpace.self, Occupancy.self, Seed.self, Desire.self, PlannedPlanting.self, Garden.self], inMemory: true)
    }
}
