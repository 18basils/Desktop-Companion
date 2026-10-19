//
//  AvatarStudioView.swift
//  Apple Companion (iOS & macOS)
//

import SwiftUI
import PhotosUI

public struct AvatarStudioView: View {
    @ObservedObject var vm: CompanionViewModel
    @State private var selectedItem: PhotosPickerItem? = nil

    private let columns = [
        GridItem(.adaptive(minimum: 150), spacing: 14)
    ]

    public var body: some View {
        VStack(spacing: 16) {
            // Dynamic Mode Card
            VStack(alignment: .leading, spacing: 10) {
                HStack {
                    VStack(alignment: .leading, spacing: 2) {
                        Text("Dynamic Avatar Cycling")
                            .font(.system(size: 15, weight: .bold))
                            .foregroundColor(.white)
                        Text("Automatically cycles through your companions on each reminder")
                            .font(.system(size: 11))
                            .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                    }
                    Spacer()
                    Toggle("", isOn: $vm.config.dynamicAvatar)
                        .labelsHidden()
                        .toggleStyle(SwitchToggleStyle(tint: Color(red: 0.22, green: 0.83, blue: 0.94)))
                }
            }
            .padding(18)
            .background(
                RoundedRectangle(cornerRadius: 18)
                    .fill(Color(red: 0.08, green: 0.12, blue: 0.20).opacity(0.75))
                    .overlay(
                        RoundedRectangle(cornerRadius: 18)
                            .stroke(Color.white.opacity(0.08), lineWidth: 1)
                    )
            )

            // Companion Collection Grid
            VStack(alignment: .leading, spacing: 12) {
                Text("Select Primary Companion")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundColor(.white)

                LazyVGrid(columns: columns, spacing: 14) {
                    ForEach(PetSkinType.allCases) { skin in
                        let isSelected = !vm.config.dynamicAvatar && vm.config.selectedSkinKey == skin.rawValue
                        Button(action: {
                            vm.setSkin(skin)
                        }) {
                            VStack(spacing: 10) {
                                ZStack {
                                    Circle()
                                        .fill(skin.primaryColor.opacity(0.2))
                                        .frame(width: 54, height: 54)
                                    Image(systemName: skin.iconName)
                                        .font(.system(size: 26))
                                        .foregroundColor(skin.primaryColor)
                                }

                                Text(skin.displayName)
                                    .font(.system(size: 13, weight: .bold))
                                    .foregroundColor(.white)

                                Text(skin.tagline)
                                    .font(.system(size: 10))
                                    .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))
                                    .multilineTextAlignment(.center)
                                    .lineLimit(2)
                            }
                            .frame(maxWidth: .infinity)
                            .padding(14)
                            .background(
                                RoundedRectangle(cornerRadius: 14)
                                    .fill(isSelected ? skin.primaryColor.opacity(0.15) : Color.white.opacity(0.04))
                                    .overlay(
                                        RoundedRectangle(cornerRadius: 14)
                                            .stroke(isSelected ? skin.primaryColor : Color.white.opacity(0.08), lineWidth: isSelected ? 2 : 1)
                                    )
                            )
                        }
                        .buttonStyle(PlainButtonStyle())
                    }
                }
            }
            .padding(18)
            .background(
                RoundedRectangle(cornerRadius: 18)
                    .fill(Color(red: 0.08, green: 0.12, blue: 0.20).opacity(0.75))
                    .overlay(
                        RoundedRectangle(cornerRadius: 18)
                            .stroke(Color.white.opacity(0.08), lineWidth: 1)
                    )
            )

            // Custom Avatar Importer Card
            VStack(alignment: .leading, spacing: 12) {
                Text("Import Custom Avatar (.gif or .png)")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundColor(.white)

                Text("Apple Sandbox Security: Photos & Files picker is strictly scoped to local user selection with zero network telemetry.")
                    .font(.system(size: 11))
                    .foregroundColor(Color(red: 0.58, green: 0.64, blue: 0.72))

                #if os(iOS)
                PhotosPicker(selection: $selectedItem, matching: .images) {
                    HStack {
                        Image(systemName: "photo.badge.plus")
                        Text("Choose from Photos...")
                    }
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 12)
                    .background(Color.white.opacity(0.08))
                    .cornerRadius(10)
                }
                .onChange(of: selectedItem) { newItem in
                    Task {
                        if let data = try? await newItem?.loadTransferable(type: Data.self) {
                            vm.config.customAvatarData = data
                            HapticAndSoundService.playSuccess(hapticsEnabled: vm.config.hapticEnabled)
                        }
                    }
                }
                #elseif os(macOS)
                Button(action: importMacAvatar) {
                    HStack {
                        Image(systemName: "folder.badge.plus")
                        Text("Browse Mac Files...")
                    }
                    .font(.system(size: 14, weight: .semibold))
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 10)
                    .background(Color.white.opacity(0.08))
                    .cornerRadius(10)
                }
                .buttonStyle(PlainButtonStyle())
                #endif
            }
            .padding(18)
            .background(
                RoundedRectangle(cornerRadius: 18)
                    .fill(Color(red: 0.08, green: 0.12, blue: 0.20).opacity(0.75))
                    .overlay(
                        RoundedRectangle(cornerRadius: 18)
                            .stroke(Color.white.opacity(0.08), lineWidth: 1)
                    )
            )
        }
    }

    #if os(macOS)
    private func importMacAvatar() {
        let panel = NSOpenPanel()
        panel.allowsMultipleSelection = false
        panel.canChooseDirectories = false
        panel.allowedContentTypes = [.gif, .png]
        if panel.runModal() == .OK, let url = panel.url, let data = try? Data(contentsOf: url) {
            // Security limit: 15MB max
            if data.count < 15 * 1024 * 1024 {
                vm.config.customAvatarData = data
                HapticAndSoundService.playSuccess(hapticsEnabled: vm.config.hapticEnabled)
            }
        }
    }
    #endif
}
