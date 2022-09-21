import 'package:flutter/material.dart';
import 'package:flutter_android_app/settings_screen.dart';
import 'package:flutter_android_app/home_page.dart';
import 'package:flutter_android_app/alarm_page.dart';
import 'package:flutter_android_app/background_service_notifications.dart';
// import 'package:flutter_windowmanager/flutter_windowmanager.dart';
// import 'package:flutter_background_service/flutter_background_service.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await initializeService();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // debugShowCheckedModeBanner: false,
      title: 'Camera Surveillance System',
      theme: ThemeData(
        primarySwatch: Colors.grey,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const HomePage(),
        '/settings': (context) => SettingsScreen(),
        '/alarm': (context) => AlarmPage(),
      },
    );
  }
}
