import Foundation
import UIKit

enum PhotoStore {
    static func photosDirectory() throws -> URL {
        let documentsDirectory = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let photosDirectory = documentsDirectory.appendingPathComponent("PlantPhotos", isDirectory: true)
        if !FileManager.default.fileExists(atPath: photosDirectory.path) {
            try FileManager.default.createDirectory(at: photosDirectory, withIntermediateDirectories: true)
        }
        return photosDirectory
    }

    static func saveImage(_ image: UIImage, fileName: String) throws -> URL {
        let directory = try photosDirectory()
        let fileURL = directory.appendingPathComponent(fileName)
        guard let imageData = image.jpegData(compressionQuality: 0.85) else {
            throw NSError(domain: "PhotoStore", code: 1, userInfo: [NSLocalizedDescriptionKey: "Failed to convert image to JPEG"])
        }
        try imageData.write(to: fileURL, options: .atomic)
        return fileURL
    }

    static func loadImage(fileName: String) -> UIImage? {
        guard let directory = try? photosDirectory() else { return nil }
        let fileURL = directory.appendingPathComponent(fileName)
        guard let imageData = try? Data(contentsOf: fileURL) else { return nil }
        return UIImage(data: imageData)
    }

    static func deleteImage(fileName: String) throws {
        let directory = try photosDirectory()
        let fileURL = directory.appendingPathComponent(fileName)
        if FileManager.default.fileExists(atPath: fileURL.path) {
            try FileManager.default.removeItem(at: fileURL)
        }
    }
}
