//
//  MacOSPetOverlayView.swift
//  Apple Companion (macOS Desktop Pet Overlay)
//

#if os(macOS)
import SwiftUI
import AppKit

public struct MacOSPetOverlayView: View {
    @ObservedObject var vm: CompanionViewModel
    @State private var petX: CGFloat = 80
    @State private var isFacingLeft: Bool = false
    @State private var showBubble: Bool = true
    @State private var walkTimer: Timer? = nil

    public var body: some View {
        let skin = vm.activeSkin()
        let hasSunglasses = vm.config.cupsToday >= 4
        let hasCrown = vm.config.cupsToday >= vm.config.dailyGoalCups

        VStack(alignment: .leading, spacing: 6) {
            // Dark Glassmorphic Speech Bubble
            if showBubble {
                VStack(spacing: 6) {
                    // Badge
                    Text("🥛 \(vm.config.cupsToday) / \(vm.config.dailyGoalCups) Cups Today")
                        .font(.system(size: 10, weight: .bold))
                        .foregroundColor(Color(red: 0.22, green: 0.83, blue: 0.94))
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .background(
                            Capsule()
                                .fill(Color(red: 0.22, green: 0.83, blue: 0.94).opacity(0.18))
                                .overlay(
                                    Capsule()
                                        .stroke(Color(red: 0.22, green: 0.83, blue: 0.94).opacity(0.3), lineWidth: 1)
                                )
                        )

                    Text(vm.emotionText)
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundColor(.white)
                        .multilineTextAlignment(.center)
                        .lineLimit(2)

                    HStack(spacing: 8) {
                        Button("YES 💧") {
                            withAnimation {
                                vm.logCup()
                                showBubble = false
                                DispatchQueue.main.asyncAfter(deadline: .now() + 4) {
                                    showBubble = true
                                }
                            }
                        }
                        .font(.system(size: 11, weight: .bold))
                        .foregroundColor(Color(red: 0.04, green: 0.07, blue: 0.13))
                        .padding(.horizontal, 14)
                        .padding(.vertical, 5)
                        .background(
                            LinearGradient(
                                colors: [
                                    Color(red: 0.13, green: 0.65, blue: 0.94),
                                    Color(red: 0.22, green: 0.83, blue: 0.94)
                                ],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .cornerRadius(6)

                        Button("Later ⏰") {
                            withAnimation {
                                showBubble = false
                            }
                        }
                        .font(.system(size: 11, weight: .medium))
                        .foregroundColor(Color(red: 0.75, green: 0.80, blue: 0.88))
                        .padding(.horizontal, 10)
                        .padding(.vertical, 5)
                        .background(Color.white.opacity(0.08))
                        .cornerRadius(6)
                    }
                }
                .padding(12)
                .background(
                    RoundedRectangle(cornerRadius: 12)
                        .fill(Color(red: 0.06, green: 0.09, blue: 0.16).opacity(0.95))
                        .overlay(
                            RoundedRectangle(cornerRadius: 12)
                                .stroke(Color(red: 0.22, green: 0.83, blue: 0.94).opacity(0.4), lineWidth: 1.5)
                        )
                        .shadow(color: Color.black.opacity(0.5), radius: 12, x: 0, y: 6)
                )
                .frame(width: 240)
            }

            // Walking Pixel Avatar Pet
            HStack {
                ZStack(alignment: .top) {
                    Image(systemName: skin.iconName)
                        .resizable()
                        .scaledToFit()
                        .frame(width: 52, height: 52)
                        .foregroundColor(skin.primaryColor)
                        .scaleEffect(x: isFacingLeft ? -1 : 1, y: 1)
                        .shadow(color: skin.primaryColor.opacity(0.5), radius: 8)

                    if hasCrown {
                        Text("👑")
                            .font(.system(size: 18))
                            .offset(y: -14)
                    }
                    if hasSunglasses {
                        Text("🕶️")
                            .font(.system(size: 16))
                            .offset(y: 10)
                    }

                    ForEach(vm.hearts) { heart in
                        Text("❤️")
                            .font(.system(size: 18))
                            .scaleEffect(heart.scale)
                            .offset(heart.offset)
                    }
                }
                .onTapGesture {
                    withAnimation {
                        vm.petCompanion()
                    }
                }
                .offset(x: petX)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .bottomLeading)
        .padding(.leading, 20)
        .padding(.bottom, 20)
        .onAppear {
            startWalking()
        }
        .onDisappear {
            walkTimer?.invalidate()
        }
    }

    private func startWalking() {
        walkTimer = Timer.scheduledTimer(withTimeInterval: 0.08, repeats: true) { _ in
            if isFacingLeft {
                petX -= 2
                if petX <= 20 {
                    isFacingLeft = false
                }
            } else {
                petX += 2
                if petX >= 180 {
                    isFacingLeft = true
                }
            }
        }
    }
}
#endif
