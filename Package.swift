// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "SoilAndSupper",
    platforms: [
        .macOS(.v14),
        .iOS(.v17)
    ],
    products: [
        .library(name: "SoilAndSupper", targets: ["SoilAndSupper"])
    ],
    targets: [
        .target(
            name: "SoilAndSupper",
            path: ".",
            sources: [
                "Models/Crop.swift",
                "Models/Garden.swift",
                "Models/GrowingSpace.swift",
                "Models/Seed.swift",
                "Models/Desire.swift",
                "Models/Occupancy.swift",
                "Models/PlannedPlanting.swift",
                "Services/CropKnowledge.swift",
                "Services/PlanningEngine.swift"
            ]
        ),
        .testTarget(
            name: "SoilAndSupperTests",
            dependencies: ["SoilAndSupper"],
            path: "Tests"
        )
    ]
)
