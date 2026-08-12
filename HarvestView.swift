import SwiftUI
import SwiftData

struct HarvestInventoryItem: Identifiable {
    let id: String
    let cropName: String
    let unit: String
    let totalQuantity: Double
    let harvests: [Harvest]
}

struct HarvestView: View {
    @Query private var allHarvests: [Harvest]
    @Environment(\.modelContext) private var modelContext

    private var inventoryItems: [HarvestInventoryItem] {
        let grouped = Dictionary(grouping: allHarvests) { harvest in
            "\(harvest.cropName)|\(harvest.unit)"
        }

        return grouped.map { key, harvests in
            let parts = key.split(separator: "|", maxSplits: 1)
            let cropName = parts.first.map(String.init) ?? ""
            let unit = parts.last.map(String.init) ?? ""
            let totalQuantity = harvests.reduce(0) { $0 + $1.quantity }
            return HarvestInventoryItem(
                id: key,
                cropName: cropName,
                unit: unit,
                totalQuantity: totalQuantity,
                harvests: harvests
            )
        }
        .sorted { $0.cropName < $1.cropName }
    }

    var body: some View {
        NavigationStack {
            List {
                if inventoryItems.isEmpty {
                    ContentUnavailableView(
                        "No Harvests",
                        systemImage: "basket",
                        description: Text("Harvests will appear here as you record them.")
                    )
                } else {
                    ForEach(inventoryItems) { item in
                        NavigationLink(value: item) {
                            HStack {
                                VStack(alignment: .leading) {
                                    Text(item.cropName)
                                        .font(.headline)
                                    Text("\(item.totalQuantity, specifier: "%.1f") \(item.unit)")
                                        .font(.subheadline)
                                        .foregroundStyle(.secondary)
                                }
                                Spacer()
                            }
                        }
                    }
                }
            }
            .navigationTitle("Harvest")
            .navigationDestination(for: HarvestInventoryItem.self) { item in
                HarvestDetailView(inventoryItem: item)
            }
        }
    }
}

struct HarvestDetailView: View {
    let inventoryItem: HarvestInventoryItem

    private var sortedHarvests: [Harvest] {
        inventoryItem.harvests.sorted { $0.date > $1.date }
    }

    var body: some View {
        List {
            ForEach(sortedHarvests) { harvest in
                VStack(alignment: .leading, spacing: 4) {
                    Text("\(harvest.quantity, specifier: "%.1f") \(harvest.unit)")
                        .font(.headline)
                    Text(harvest.date, format: .dateTime.day().month().year())
                        .font(.caption)
                        .foregroundStyle(.secondary)
                    if let notes = harvest.notes, !notes.isEmpty {
                        Text(notes)
                            .font(.body)
                    }
                }
            }
        }
        .navigationTitle(inventoryItem.cropName)
    }
}

struct HarvestView_Previews: PreviewProvider {
    static var previews: some View {
        HarvestView()
    }
}
