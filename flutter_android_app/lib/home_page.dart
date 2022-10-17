import 'package:device_apps/device_apps.dart';
import 'package:flutter/material.dart';
import 'package:flutter_background_service/flutter_background_service.dart';
import 'package:flutter_android_app/background_service_notifications.dart';
import 'package:flutter_android_app/image_connection.dart';
import 'package:flutter_android_app/triggers_notifications.dart';
import 'package:flutter_android_app/logger.dart';
import 'package:flutter_windowmanager/flutter_windowmanager.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with WidgetsBindingObserver {
  final imageConnection =
      ImageConnection(FlutterBackgroundService().on('onUpdateState'));
  final _triggersNotifications = TriggersNotifications();
  bool _gridOn = false;
  AppLifecycleState? appLifecycleState;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);

    print('home_page initState() called');
    Future.delayed(const Duration(seconds: 2),
        () => appLifecycleState = AppLifecycleState.resumed);

    imageConnection.addListener(() => setState(() {
          // _frameCount++;
        }));

    FlutterBackgroundService()
        .on('alarmReceived')
        .listen((Map<String, dynamic>? triggerInfo) async {
      await FlutterWindowManager.addFlags(
          FlutterWindowManager.FLAG_SHOW_WHEN_LOCKED);
      await FlutterWindowManager.addFlags(
          FlutterWindowManager.FLAG_TURN_SCREEN_ON);
      // print('[home_page] alarmReceived received');

      // TODO: Send image to alarm page
      // triggerInfo?['frame'] = imageConnection.frameReceived;

      print('appLifecycleState: $appLifecycleState');
      if (appLifecycleState == AppLifecycleState.paused) {
        DeviceApps.openApp('dev.eduardonn.sursystem_android_app');
      }

      Navigator.pushNamed(context, '/alarm', arguments: triggerInfo);
    });

    // FlutterBackgroundService().invoke("appOpened"); // TODO: Activate
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    print('[Home Page] Dispose called');
    imageConnection.stop();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    appLifecycleState = state;
    switch (state) {
      case AppLifecycleState.resumed:
        imageConnection.start();
        break;
      default:
        imageConnection.stop();
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        actions: [
          RawMaterialButton(
            onPressed: () => Navigator.pushNamed(context, '/settings'),
            child: const Padding(
              padding: EdgeInsets.all(8.0),
              child: Icon(
                Icons.settings,
                size: 36,
              ),
            ),
          ),
          RawMaterialButton(
            onPressed: () => Navigator.pushNamed(context, '/alarm',
                arguments: {'local': 'Teste'}),
            child: const Padding(
              padding: EdgeInsets.all(8.0),
              child: Icon(
                Icons.notifications_active,
                size: 36,
              ),
            ),
          ),
        ],
        title: const Text('Camera Surveillance System'),
      ),
      backgroundColor: Colors.grey[400],
      body: Column(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              MaterialButton(
                  padding: const EdgeInsets.all(12.0),
                  child: const Icon(Icons.notifications),
                  onPressed: () async {
                    await Future.delayed(const Duration(seconds: 6));
                    _triggersNotifications.notify('title teste', 'body teste');
                  }),
              // MaterialButton(
              //   padding: EdgeInsets.all(12.0),
              //   child: Icon(Icons.refresh),
              //   onPressed: () => imageConnection._connect(),
              // ),
            ],
          ),
          if (_gridOn)
            OrientationBuilder(
              builder: (context, orientation) {
                if (orientation == Orientation.portrait) {
                  return Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      _imageWidget(),
                      _imageWidget(),
                    ],
                  );
                } else {
                  return Row(
                    children: [
                      _imageWidget(),
                      _imageWidget(),
                    ],
                  );
                }
              },
            )
          else
            _imageWidget(),
          // Card(
          //   child: Text(
          //     // controller: logTextController,
          //     // minLines: 8,
          //     maxLines: 8,

          //   ),
          // ),
          // Spacer(),
          Flexible(
            child: GridView.count(
              shrinkWrap: true,
              childAspectRatio: 12 / 2.5,
              clipBehavior: Clip.none,
              crossAxisCount: 2,
              children: <Widget>[
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: ElevatedButton(
                    child: const Text("Is App Running"),
                    onPressed: () async {
                      Logger.log(
                          '[From Service] is running: ${await FlutterBackgroundService().isRunning()}');
                    },
                  ),
                ),
                Container(
                  padding: const EdgeInsets.all(8.0),
                  child: ElevatedButton(
                    child: const Text("Force Start Service"),
                    onPressed: () {
                      initializeService(true);
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: ElevatedButton(
                    child: const Text("Stop Service"),
                    onPressed: () {
                      FlutterBackgroundService().invoke("stopService");
                      imageConnection.stop();
                    },
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: ElevatedButton(
                    child: const Text("Send appOpened"),
                    onPressed: () {
                      FlutterBackgroundService().invoke("appOpened");
                      imageConnection.stop();
                    },
                  ),
                ),
              ],
            ),
          ),
          Expanded(child: Logger()),
          // const Spacer(),
          Container(
            margin: const EdgeInsets.only(top: 12.0),
            padding: const EdgeInsets.all(5.0),
            child: Row(
              children: [
                Row(
                  children: <Widget>[
                    const Text(
                      'Data packets discarded: ',
                      style: TextStyle(
                        fontSize: 12,
                        decoration: TextDecoration.none,
                        color: Colors.black,
                      ),
                    ),
                    StreamBuilder<int>(
                        stream: imageConnection.imageReceiver
                            .timesFrameNotFoundStreamController.stream,
                        builder: (context, snapshot) {
                          return Text(
                            '${snapshot.data}',
                            style: const TextStyle(
                              fontSize: 12,
                              decoration: TextDecoration.none,
                              color: Colors.black,
                            ),
                          );
                        }),
                  ],
                ),
                const Spacer(),
                StreamBuilder<Map<String, dynamic>?>(
                  stream: FlutterBackgroundService().on('onUpdateState'),
                  builder: (context, snapshot) {
                    if (!snapshot.hasData) {
                      return stateText('Disconnected', Colors.red);
                    }

                    final data = snapshot.data!;

                    switch (ConnectionState.values[data['state']]) {
                      case ConnectionState.done:
                        return stateText('Connected', Colors.green);
                      case ConnectionState.waiting:
                        return stateText('Trying to Connect', Colors.blue);
                      default:
                        return stateText('Disconnected', Colors.red);
                    }
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Text stateText(String text, Color color) {
    return Text(
      text,
      style: TextStyle(
        color: color,
      ),
    );
  }

  Widget _imageWidget() {
    return GestureDetector(
      onTap: () => setState(() => _gridOn = !_gridOn),
      child: imageConnection.frame ??
          AspectRatio(
            aspectRatio: 16 / 9,
            child: Container(
              color: Colors.black,
              margin: const EdgeInsets.all(2.0),
              child: const Center(
                child: Text(
                  'No Signal',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 32.0,
                  ),
                ),
              ),
            ),
          ),
    );
  }
}
