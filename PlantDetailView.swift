import SwiftUI
import SwiftData
import PhotosUI

struct PlantDetailView: View {
    @Bindable var plant: Plant
    @Environment(\.modelContext) private var modelContext
    @Query private var allPhotos: [PlantPhoto]
    @State private var showingPhotoPicker = false
    @State private var selectedPhotoItem: PhotosPickerItem? = nil
    @State private var showingJournalEntry = false
    @State private var editingEntry: JournalEntry? = nil
    @State private var showingHarvest = false
    @State private var editingHarvest: Harvest? = nil

    private var plantPhotos: [PlantPhoto] {
        allPhotos.filter { $0.plant?.id == plant.id }
    }

    private var sortedJournalEntries: [JournalEntry] {
        plant.journalEntries.sorted { $0.date > $1.date }
    }

    private var sortedHarvests: [Harvest] {
        plant.harvests.sorted { $0.date > $1.date }
    }

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

            Section("Photos") {
                if plantPhotos.isEmpty {
                    ContentUnavailableView(
                        "No Photos",
                        systemImage: "photo",
                        description: Text("Tap + to add your first photo.")
                    )
                } else {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 12) {
                            ForEach(plantPhotos) { photo in
                                if let image = PhotoStore.loadImage(fileName: photo.fileName) {
                                    Image(uiImage: image)
                                        .resizable()
                                        .scaledToFill()
                                        .frame(width: 120, height: 120)
                                        .clipped()
                                        .cornerRadius(8)
                                        .contextMenu {
                                            Button("Delete", role: .destructive) {
                                                deletePhoto(photo)
                                            }
                                        }
                                }
                            }
                        }
                        .padding(.vertical, 4)
                    }
                }
            }

            Section("Journal") {
                if sortedJournalEntries.isEmpty {
                    ContentUnavailableView(
                        "No Journal Entries",
                        systemImage: "book",
                        description: Text("Tap + to add your first entry.")
                    )
                } else {
                    ForEach(sortedJournalEntries) { entry in
                        VStack(alignment: .leading, spacing: 4) {
                            Text(entry.date, format: .dateTime.day().month().year())
                                .font(.caption)
                                .foregroundStyle(.secondary)
                            Text(entry.text)
                                .font(.body)
                        }
                        .swipeActions(edge: .trailing, allowsFullSwipe: false) {
                            Button("Edit") {
                                editingEntry = entry
                                showingJournalEntry = true
                            }
                            Button("Delete", role: .destructive) {
                                modelContext.delete(entry)
                            }
                        }
                    }
                }
            }

            Section("Harvests") {
                if sortedHarvests.isEmpty {
                    ContentUnavailableView(
                        "No Harvests",
                        systemImage: "basket",
                        description: Text("Tap + to add your first harvest.")
                    )
                } else {
                    ForEach(sortedHarvests) { harvest in
                        VStack(alignment: .leading, spacing: 4) {
                            Text("\(harvest.cropName) — \(harvest.quantity, specifier: "%.1f") \(harvest.unit)")
                                .font(.body)
                            Text(harvest.date, format: .dateTime.day().month().year())
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                        .swipeActions(edge: .trailing, allowsFullSwipe: false) {
                            Button("Edit") {
                                editingHarvest = harvest
                                showingHarvest = true
                            }
                            Button("Delete", role: .destructive) {
                                modelContext.delete(harvest)
                            }
                        }
                    }
                }
            }
        }
        .navigationTitle(plant.name)
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Menu {
                    Button {
                        showingPhotoPicker = true
                    } label: {
                        Label("Add Photo", systemImage: "photo")
                    }
                    Button {
                        editingEntry = nil
                        showingJournalEntry = true
                    } label: {
                        Label("Add Journal Entry", systemImage: "square.and.pencil")
                    }
                    Button {
                        editingHarvest = nil
                        showingHarvest = true
                    } label: {
                        Label("Add Harvest", systemImage: "basket")
                    }
                } label: {
                    Label("Add", systemImage: "plus")
                }
            }
            ToolbarItem(placement: .destructiveAction) {
                Button("Delete") {
                    modelContext.delete(plant)
                }
            }
        }
        .photosPicker(
            isPresented: $showingPhotoPicker,
            selection: $selectedPhotoItem,
            matching: .images
        )
        .onChange(of: selectedPhotoItem) { _, newItem in
            guard let newItem = newItem else { return }
            Task {
                await handlePhotoSelection(newItem)
            }
        }
        .sheet(isPresented: $showingJournalEntry, onDismiss: {
            editingEntry = nil
        }) {
            JournalEntryView(plant: plant, entry: editingEntry)
        }
        .sheet(isPresented: $showingHarvest, onDismiss: {
            editingHarvest = nil
        }) {
            AddEditHarvestView(plant: plant, harvest: editingHarvest)
        }
        .onDisappear {
            plant.updatedAt = Date()
        }
    }

    private func handlePhotoSelection(_ item: PhotosPickerItem) async {
        guard let data = try? await item.loadTransferable(type: Data.self),
              let uiImage = UIImage(data: data) else {
            selectedPhotoItem = nil
            return
        }

        let fileName = UUID().uuidString + ".jpg"
        do {
            _ = try PhotoStore.saveImage(uiImage, fileName: fileName)
            let photo = PlantPhoto(fileName: fileName)
            photo.plant = plant
            modelContext.insert(photo)
        } catch {
            print("Failed to save photo: \(error)")
        }

        selectedPhotoItem = nil
    }

    private func deletePhoto(_ photo: PlantPhoto) {
        do {
            try PhotoStore.deleteImage(fileName: photo.fileName)
        } catch {
            print("Failed to delete photo file: \(error)")
        }
        modelContext.delete(photo)
    }
}

struct PlantDetailView_Previews: PreviewProvider {
    static var previews: some View {
        PlantDetailView(plant: Plant(name: "Tomato"))
    }
}
