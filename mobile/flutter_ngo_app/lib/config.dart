// Configuration for API base URL
// 10.0.2.2:8000 - Android emulator localhost
// 192.168.7.2:8000 - Your computer's IP for real device testing
// Change this IP to match your computer's local network IP

import 'dart:io';

String get API_BASE {
  // Check if running on Android emulator
  if (Platform.isAndroid) {
    // You can detect emulator vs real device, but for simplicity:
    // Use your computer's actual IP address for real device testing
    return 'http://192.168.7.2:8000';
  }
  // For iOS simulator, use localhost
  return 'http://127.0.0.1:8000';
}

// Alternative: You can also create separate configurations
const String API_BASE_EMULATOR = 'http://10.0.2.2:8000';
const String API_BASE_DEVICE = 'http://192.168.7.2:8000';
const String API_BASE_IOS = 'http://127.0.0.1:8000';
