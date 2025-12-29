// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_ngo_app/main.dart';

void main() {
  testWidgets('App boots to Login screen', (WidgetTester tester) async {
    // Build the app and trigger a frame.
    await tester.pumpWidget(const BlueCarbonMRVApp());

    // Verify a stable piece of UI from the Login screen is present.
    expect(find.text('Sign In'), findsAtLeastNWidgets(1));
    expect(find.text('Blue Carbon MRV'), findsOneWidget);
  });
}
