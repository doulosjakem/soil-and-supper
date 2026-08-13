import SwiftUI
import SwiftData
import PhotosUI
import UIKit

struct IdentifyView: View {
    @Query private var photos: [PlantPhoto]
    @Environment(\.modelContext) private var modelContext
    @EnvironmentObject private var plantIdentifier: MockPlantIdentifier

    @State private var selectedPhoto: PlantPhoto?
    @State private var isIdentifying = false
    @State private var identification: PlantIdentification?
    @State private var isCorrecting = false
    @State private var correctedName = ""
    @State private var saveMessage: String?

    var body: some View {
        NavigationStack {
            List {
                if photos.isEmpty {
                    ContentUnavailableView(
                        "No Photos",
                        systemImage: "photo",
                        description: Text("Add photos to plants first, then use them for identification.")
                    )
                } else {
                    ForEach(photos) { photo in
                        if let image = PhotoStore.loadImage(fileName: photo.fileName) {
                            Button {
                                selectedPhoto = photo
                                startIdentification(photo)
                            } label: {
                                HStack {
                                    Image(uiImage: image)
                                        .resizable()
                                        .scaledToFill()
                                        .frame(width: 50, height: 50)
                                        .clipped()
                                        .cornerRadius(6)
                                    VStack(alignment: .leading) {
                                        Text(photo.plant?.name ?? "Unidentified plant")
                                            .font(.headline)
                                        if let plant = photo.plant {
                                            Text("Linked to plant")
                                                .font(.caption)
                                                .foregroundStyle(.secondary)
                                        } else {
                                            Text("Not linked to a plant")
                                                .font(.caption)
                                                .foregroundStyle(.secondary)
                                        }
                                    }
                                    Spacer()
                                }
                            }
                        }
                    }
                }
            }
            .navigationTitle("Identify")
            .sheet(item: $selectedPhoto) { photo in
                IdentificationResultView(
                    photo: photo,
                    isIdentifying: $isIdentifying,
                    identification: $identification,
                    isCorrecting: $isCorrecting,
                    correctedName: $correctedName,
                    saveMessage: $saveMessage,
                    plantIdentifier: plantIdentifier,
                    modelContext: modelContext
                )
                .onDisappear {
                    isIdentifying = false
                    identification = nil
                    isCorrecting = false
                    correctedName = ""
                    saveMessage = nil
                }
            }
        }
    }

    private func startIdentification(_ photo: PlantPhoto) {
        isIdentifying = true
        identification = nil
        isCorrecting = false
        correctedName = ""
        saveMessage = nil

        Task {
            guard let image = PhotoStore.loadImage(fileName: photo.fileName) else {
                isIdentifying = false
                return
            }

            do {
                let result = try await plantIdentifier.identify(image: image)
                await MainActor.run {
                    identification = result
                    correctedName = result.cropName
                    isIdentifying = false
                }
            } catch {
                await MainActor.run {
                    isIdentifying = false
                    saveMessage = "Identification failed: \(error.localizedDescription)"
                }
            }
        }
    }
}

struct IdentificationResultView: View {
    let photo: PlantPhoto
    @Binding var isIdentifying: Bool
    @Binding var identification: PlantIdentification?
    @Binding var isCorrecting: Bool
    @Binding var correctedName: String
    @Binding var saveMessage: String?

    let plantIdentifier: MockPlantIdentifier
    let modelContext: ModelContext

    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            Form {
                if let image = PhotoStore.loadImage(fileName: photo.fileName) {
                    Section("Photo") {
                        Image(uiImage: image)
                            .resizable()
                            .scaledToFit()
                            .frame(maxHeight: 250)
                            .clipShape(RoundedRectangle(cornerRadius: 8))
                    }
                }

                if isIdentifying {
                    Section("Result") {
                        HStack {
                            Spacer()
                            ProgressView()
                            Spacer()
                        }
                    }
                } else if let identification = identification {
                    Section("Result") {
                        if isCorrecting {
                            TextField("Plant Name", text: $correctedName)
                        } else {
                            Text(identification.cropName)
                                .font(.title3)
                                .fontWeight(.semibold)
                            if let variety = identification.variety, !variety.isEmpty {
                                Text(variety)
                                    .font(.subheadline)
                                    .foregroundStyle(.secondary)
                            }
                            Text("Confidence: \(Int(identification.confidence * 100))%")
                                .font(.caption)
                                .foregroundStyle(.secondary)
                        }
                    }

                    Section {
                        if isCorrecting {
                            Button("Save Correction") {
                                saveResult(cropName: correctedName)
                            }
                            .disabled(correctedName.trimmingCharacters(in: .whitespaces).isEmpty)
                        } else {
                            Button("Confirm Identification") {
                                saveResult(cropName: identification.cropName)
                            }

                            Button("Correct Result") {
                                isCorrecting = true
                            }
                        }
                    }
                }

                if let saveMessage = saveMessage {
                    Section {
                        Text(saveMessage)
                            .font(.footnote)
                            .foregroundStyle(.secondary)
                    }
                }
            }
            .navigationTitle("Identify Plant")
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") {
                        dismiss()
                    }
                }
            }
        }
    }

    private func saveResult(cropName: String) {
        let trimmedName = cropName.trimmingCharacters(in: .whitespaces)
        guard !trimmedName.isEmpty else { return }

        if let existingPlant = photo.plant {
            existingPlant.name = trimmedName
            existingPlant.updatedAt = Date()
        } else {
            let newPlant = Plant(name: trimmedName)
            photo.plant = newPlant
            modelContext.insert(newPlant)
        }

        saveMessage = "Saved: \(trimmedName)"
    }
}

#Preview {
    IdentifyView()
        .modelContainer(for: [Plant.self, PlantPhoto.self], inMemory: true)
        .environmentObject(MockPlantIdentifier())
}
