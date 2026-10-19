//
//  macOSApp.swift
//  Apple Companion (macOS Target)
//

#if os(macOS)
import SwiftUI
import AppKit

@main
struct MacOSCompanionApp: App {
    @StateObject private var vm = CompanionViewModel()
    @NSApplicationDelegateAdaptor(MacAppDelegate.self) var appDelegate

    var body: some Scene {
        // 1. MenuBarExtra: Native macOS top Menu Bar icon (Matches Windows System Tray)
        MenuBarExtra("Desktop Companion", systemImage: "drop.fill") {
            VStack {
                Button("💧 Summon Companion to Desktop") {
                    appDelegate.showFloatingOverlay(vm: vm)
                }

                Button("🥛 Log Cup of Water (\(vm.config.cupsToday)/\(vm.config.dailyGoalCups))") {
                    vm.logCup()
                }

                Divider()

                // Avatars Submenu
                Menu("🎨 Avatars & Skins") {
                    Toggle("✨ Dynamic Auto-Cycle", isOn: $vm.config.dynamicAvatar)
                    Divider()
                    ForEach(PetSkinType.allCases) { skin in
                        Button(skin.displayName) {
                            vm.setSkin(skin)
                        }
                    }
                }

                // Meeting Mode / Pause Submenu
                Menu("⏸️ Meeting Mode / Pause") {
                    if let pausedUntil = vm.pausedUntil, Date() < pausedUntil {
                        Button("▶️ Resume Reminders") {
                            vm.resumeReminders()
                        }
                    } else {
                        Button("Pause for 30 minutes") { vm.pauseReminders(minutes: 30) }
                        Button("Pause for 1 hour") { vm.pauseReminders(minutes: 60) }
                        Button("Pause for 2 hours") { vm.pauseReminders(minutes: 120) }
                    }
                }

                // Schedule & Quiet Hours
                Menu("📅 Schedule & Quiet Hours") {
                    Toggle("🌙 Quiet Hours (\(vm.config.quietHours.formattedRange))", isOn: $vm.config.quietHours.enabled)
                }

                Divider()

                // Open Main Studio Window
                Button("⚙️ Open Studio Settings...") {
                    appDelegate.openMainWindow()
                }

                Divider()

                Button("❌ Quit Desktop Companion") {
                    NSApplication.shared.terminate(nil)
                }
            }
        }

        // 2. Main Studio Window
        WindowGroup("Desktop Companion Studio", id: "main_studio") {
            MainContentView()
                .frame(minWidth: 540, minHeight: 640)
        }
        .windowStyle(.hiddenTitleBar)
        .defaultSize(width: 580, height: 680)
    }
}

public final class MacAppDelegate: NSObject, NSApplicationDelegate {
    private var overlayWindow: NSPanel?

    public func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.accessory) // Runs quietly in menu bar without cluttering Dock
    }

    public func openMainWindow() {
        NSApp.setActivationPolicy(.regular)
        if let window = NSApp.windows.first(where: { $0.identifier?.rawValue == "main_studio" }) {
            window.makeKeyAndOrderFront(nil)
            NSApp.activate(ignoringOtherApps: true)
        } else {
            // Reopen window group
            for window in NSApp.windows {
                if window != overlayWindow {
                    window.makeKeyAndOrderFront(nil)
                    NSApp.activate(ignoringOtherApps: true)
                    return
                }
            }
        }
    }

    public func showFloatingOverlay(vm: CompanionViewModel) {
        if overlayWindow == nil {
            let panel = NSPanel(
                contentRect: NSRect(x: 100, y: 100, width: 340, height: 180),
                styleMask: [.borderless, .nonactivatingPanel],
                backing: .buffered,
                defer: false
            )
            panel.isFloatingPanel = true
            panel.level = .floating
            panel.isOpaque = false
            panel.backgroundColor = .clear
            panel.hasShadow = false
            panel.contentView = NSHostingView(rootView: MacOSPetOverlayView(vm: vm))

            // Position at bottom left of primary screen
            if let screen = NSScreen.main {
                let screenRect = screen.visibleFrame
                panel.setFrameOrigin(NSPoint(x: screenRect.minX + 40, y: screenRect.minY + 20))
            }

            self.overlayWindow = panel
        }

        overlayWindow?.orderFrontRegardless()
    }
}
#endif
