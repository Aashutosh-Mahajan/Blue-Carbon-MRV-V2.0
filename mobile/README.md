# BlueQuant - Mobile Application

Flutter-based mobile application for NGO field data collection and project management.

## Overview

This mobile app allows NGO representatives to:
- Submit new restoration projects from the field
- Upload geo-tagged images and documents
- Track project verification status
- View carbon credit balances
- Receive notifications on project updates

## Requirements

- Flutter SDK 3.0+
- Dart SDK 3.0+
- Android Studio / VS Code with Flutter extensions
- Android SDK (for Android builds)
- Xcode (for iOS builds, macOS only)

## Setup

### 1. Install Dependencies

```bash
cd mobile/flutter_ngo_app
flutter pub get
```

### 2. Configure API Endpoint

Edit `lib/config.dart`:

```dart
// For Android emulator (connects to host machine)
const String API_BASE_EMULATOR = 'http://10.0.2.2:8000';

// For physical device (use your computer's local IP)
const String API_BASE_DEVICE = 'http://192.168.x.x:8000';

// For iOS simulator
const String API_BASE_IOS = 'http://127.0.0.1:8000';
```

### 3. Run the App

```bash
# Check connected devices
flutter devices

# Run on connected device/emulator
flutter run

# Run on specific device
flutter run -d <device_id>
```

## Project Structure

```
flutter_ngo_app/
|-- lib/
|   |-- main.dart           # App entry point
|   |-- config.dart         # API configuration
|   |-- screens/
|   |   |-- login.dart      # Authentication screen
|   |   |-- dashboard.dart  # Main dashboard
|   |   |-- new_project.dart    # Project submission
|   |   +-- project_detail.dart # Project details
|   |-- theme/
|   |   +-- app_theme.dart  # App theming
|   +-- widgets/            # Reusable components
|-- assets/
|   |-- icons/              # App icons
|   +-- images/             # Static images
|-- android/                # Android-specific config
|-- ios/                    # iOS-specific config
+-- pubspec.yaml            # Dependencies
```

## Features

### Authentication
- Email/password login
- Token-based session management
- Secure credential storage

### Dashboard
- Project statistics overview
- Recent projects list
- Quick actions menu
- Credit balance display

### Project Submission
- Title and description input
- Location selection with GPS
- Species and area specification
- Image capture and upload
- Document attachment

### Project Tracking
- Real-time status updates
- Verification stage progress
- Credit issuance notifications

## Dependencies

| Package | Purpose |
|---------|---------|
| http | API communication |
| flutter_secure_storage | Secure token storage |
| image_picker | Camera/gallery access |
| geolocator | GPS location |
| permission_handler | Runtime permissions |
| fl_chart | Statistics charts |
| cached_network_image | Image caching |
| intl | Date/number formatting |

## Building for Release

### Android

```bash
# Generate release APK
flutter build apk --release

# Generate App Bundle (for Play Store)
flutter build appbundle --release
```

Output: `build/app/outputs/flutter-apk/app-release.apk`

### iOS

```bash
# Build for iOS (macOS only)
flutter build ios --release
```

## Troubleshooting

### Connection Issues

1. Ensure Django server is running
2. Check firewall allows connections on port 8000
3. Verify correct IP in `config.dart`
4. For physical devices, ensure same WiFi network

### Permission Errors

The app requires these permissions:
- Camera (for image capture)
- Location (for GPS tagging)
- Storage (for file access)

Grant permissions when prompted or in device settings.

### Build Errors

```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

## API Endpoints Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/mobile/login/` | POST | Authentication |
| `/mobile/profile/` | GET | User profile |
| `/mobile/projects/` | GET/POST | List/create projects |
| `/mobile/projects/<id>/` | GET | Project details |

## Contributing

1. Follow Flutter/Dart style guidelines
2. Test on both Android and iOS
3. Update this README for new features
