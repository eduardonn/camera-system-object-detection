import 'dart:async';
import 'dart:ui';
// import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:flutter_background_service_android/flutter_background_service_android.dart';
import 'package:device_apps/device_apps.dart';
// import 'package:shared_preferences/shared_preferences.dart';
// import 'package:url_launcher/url_launcher.dart';
import 'package:flutter_android_app/triggers_connection.dart';

Future<void> initializeService([bool forceInitialize = false]) async {
  final service = FlutterBackgroundService();
  // print('service: ${service.hashCode}');
  // if (await service.isRunning() && !forceInitialize) {
  //   debugPrint('Serviço já está em execução. Retornando...');
  //   return;
  // }
  await service.configure(
    androidConfiguration: AndroidConfiguration(
      // this will be executed when app is in foreground or background in separated isolate
      onStart: onStart,

      // auto start service
      autoStart: true,
      isForegroundMode: false,
    ),
    iosConfiguration: IosConfiguration(
      // auto start service
      autoStart: true,

      // this will be executed when app is in foreground in separated isolate
      onForeground: onStart,

      // you have to enable background fetch capability on xcode project
      onBackground: onIosBackground,
    ),
  );
  service.startService();
}

// to ensure this is executed
// run app from xcode, then from xcode menu, select Simulate Background Fetch
bool onIosBackground(ServiceInstance service) {
  WidgetsFlutterBinding.ensureInitialized();
  print('FLUTTER BACKGROUND FETCH');

  return true;
}

@pragma('vm:entry-point')
void onStart(ServiceInstance service) async {
  print('onStart called');

  // Only available for flutter 3.0.0 and later
  DartPluginRegistrant.ensureInitialized();

  // For flutter prior to version 3.0.0
  // We have to register the plugin manually

  final triggersConnection = TriggersConnection(
    onUpdateState: (ConnectionState value) {
      try {
        service.invoke(
          'onUpdateState',
          {
            "state": value.index,
          },
        );
      } catch (e) {
        print(e.toString());
      }
    },
    onTriggerAlarmReceived: (Map<String, dynamic> alarmInfo) async {
      service.invoke('alarmReceived', alarmInfo);
    },
    ifAppIsClosed: (Map<String, dynamic> alarmInfo) {
      DeviceApps.openApp('dev.eduardonn.sursystem_android_app');
    },
  );

  service.on('stopService').listen((event) {
    service.stopSelf();
  });

  service.on('serverIPUpdate').listen((event) {
    debugPrint('serverIPUpdate called');
    triggersConnection.serverIP = event?['serverIP'];
  });

  service.on('alarmConsumed').listen((event) {
    triggersConnection.alarmReceived = null;
  });

  service.on('stopRequestingVideo').listen((event) {
    triggersConnection.setRequestVideo(false);
  });

  service.on('requestVideo').listen((event) {
    triggersConnection.setRequestVideo(true);
  });

  service.on('appOpened').listen((event) {
    // If app was closed when it received an alarm, it will open now
    triggersConnection.setRequestVideo(true);

    print('[Service] appOpened event received');
    if (triggersConnection.alarmReceived == null) {
      print('[Service] no alarm has arrived');
      return;
    }

    service.invoke('alarmReceived', triggersConnection.alarmReceived);
  });

  // Timer.periodic(Duration(seconds: 5), (timer) async {
  //   print('sending \'testing\'');
  //   service.invoke(
  //       'testing', {'value': await FlutterBackgroundService().isRunning()});
  //   if (triggersConnection.alarmReceived == null) {
  //     timer.cancel();
  //     return;
  //   } else {
  //     print('[BackgroundService] invoking alarmReceived');
  //     service.invoke('alarmReceived', triggersConnection.alarmReceived);
  //   }
  // });
}
