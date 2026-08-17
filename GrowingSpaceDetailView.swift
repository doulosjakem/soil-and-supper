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
                if let spaceType = space.spaceType {
                    Text(spaceType.displayName)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
                if let width = space.width, let length = space.length {
                    Text("\(width, specifier: "%.1f") ft × \(length, specifier: "%.1f") ft")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                } else if let width = space.width {
                    Text("Width: \(width, specifier: "%.1f") ft")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                } else if let length = space.length {
                    Text("Length: \(length, specifier: "%.1f") ft")
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }
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
                                SuggestionRow(suggestion: suggestion, context: .current)
                            }
                        }

                        if !alsoGoodSuggestions.isEmpty {
                            ForEach(alsoGoodSuggestions) { suggestion in
                                SuggestionRow(suggestion: suggestion, context: .current)
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
                            Text("Growing now")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                            Text("Planted \(occupancy.startDate, format: .dateTime.day().month().year())")
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
                    Section {
                        if !futureBestFit.isEmpty {
                            ForEach(futureBestFit) { suggestion in
                                SuggestionRow(suggestion: suggestion, context: .future)
                            }
                        }

                        if !futureAlsoGood.isEmpty {
                            ForEach(futureAlsoGood) { suggestion in
                                SuggestionRow(suggestion: suggestion, context: .future)
                            }
                        }
                    } header: {
                        Text("Next")
                    } footer: {
                        Text("These are recommendations for what could follow the current crop. Planting dates depend on when the space opens.")
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

struct SuggestionRow: View {
    let suggestion: PlantingSuggestion
    let context: SuggestionContext

    enum SuggestionContext {
        case current
        case future
    }

    var body: some View {
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
                Text(rankingLabel)
                    .font(.caption)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(rankingColor.opacity(0.2))
                    .foregroundStyle(rankingColor)
                    .clipShape(Capsule())
            }

            ForEach(timingLines, id: \.self) { line in
                Text(line)
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            if let harvest = suggestion.estimatedHarvestDate {
                Text("Harvest ~\(shortDate(harvest))")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }

            Text(suggestion.reason)
                .font(.caption)
                .foregroundStyle(.secondary)

            if !suggestion.warnings.isEmpty {
                ForEach(suggestion.warnings, id: \.self) { warning in
                    Text(warning)
                        .font(.caption)
                        .foregroundStyle(.orange)
                }
            }
        }
    }

    /// Communicates the opening date and the actual candidate planting date
    /// without confusing them. When a future space opens before its planting
    /// window begins, the space-opening and planting dates are shown separately
    /// so the recommendation is never presented as currently plantable.
    private var timingLines: [String] {
        let planting = shortDate(suggestion.suggestedPlantingDate)

        guard context == .future, let opening = suggestion.openingDate else {
            return ["Plant \(planting)"]
        }

        if Calendar.current.isDate(opening, inSameDayAs: suggestion.suggestedPlantingDate) {
            return ["Plant when space opens \(planting)"]
        }

        if suggestion.suggestedPlantingDate > opening {
            return [
                "Space opens \(shortDate(opening))",
                "Plant \(planting)\(windowSuffix)"
            ]
        }

        return ["Plant \(planting)"]
    }

    private var windowSuffix: String {
        guard let name = suggestion.plantingWindowName else { return "" }
        return " (\(name) planting)"
    }

    private func shortDate(_ date: Date) -> String {
        date.formatted(.dateTime.month(.abbreviated).day())
    }

    private var rankingLabel: String {
        suggestion.ranking.label
    }

    private var rankingColor: Color {
        switch suggestion.ranking {
        case .bestFit: return .green
        case .alsoGood: return .blue
        case .notRecommended: return .orange
        }
    }
}

struct GrowingSpaceDetailView_Previews: PreviewProvider {
    static var previews: some View {
        GrowingSpaceDetailView(space: GrowingSpace(name: "Bed 1"))
            .modelContainer(for: [GrowingSpace.self, Occupancy.self, Seed.self, Desire.self, PlannedPlanting.self, Garden.self], inMemory: true)
    }
}
