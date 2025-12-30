import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'screens/login.dart';
import 'screens/dashboard.dart';
import 'screens/project_detail.dart';
import 'screens/new_project.dart';
import 'theme/app_theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // Set system UI overlay style for a professional look
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.dark,
      systemNavigationBarColor: Colors.white,
      systemNavigationBarIconBrightness: Brightness.dark,
    ),
  );

  runApp(const BlueCarbonMRVApp());
}

class BlueCarbonMRVApp extends StatelessWidget {
  const BlueCarbonMRVApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BlueQuant',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      initialRoute: '/',
      routes: {
        '/': (context) => const LoginScreen(),
        '/dashboard': (context) => const DashboardScreen(),
        '/new': (context) => const NewProjectScreen(),
      },
      onGenerateRoute: (settings) {
        if (settings.name == '/project') {
          final args = settings.arguments as Map<String, dynamic>?;
          final projectId = args?['id'] as int?;
          if (projectId != null) {
            return MaterialPageRoute(
              builder: (context) => ProjectDetailScreen(projectId: projectId),
            );
          }
        }
        return null;
      },
      builder: (context, child) {
        return MediaQuery(
          data: MediaQuery.of(context)
              .copyWith(textScaler: const TextScaler.linear(1.0)),
          child: child!,
        );
      },
    );
  }
}
