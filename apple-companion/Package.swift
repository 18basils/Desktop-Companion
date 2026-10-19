// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "AppleCompanion",
    defaultLocalization: "en",
    platforms: [
        .iOS(.v16),
        .macOS(.v13)
    ],
    products: [
        .executable(
            name: "AppleCompanion",
            targets: ["AppleCompanion"]
        )
    ],
    targets: [
        .executableTarget(
            name: "AppleCompanion",
            path: ".",
            sources: [
                "Shared",
                "iOS",
                "macOS"
            ],
            resources: [
                .process("Resources")
            ]
        )
    ]
)
