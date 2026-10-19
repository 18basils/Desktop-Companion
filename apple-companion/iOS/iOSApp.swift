//
//  iOSApp.swift
//  Apple Companion (iOS & iPadOS Target)
//

#if os(iOS)
import SwiftUI

@main
struct IOSCompanionApp: App {
    var body: some Scene {
        WindowGroup {
            MainContentView()
                .preferredColorScheme(.dark)
        }
    }
}
#endif
