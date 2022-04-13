import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // 2022-04-10 6th lecture
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('6강: 중요한 커스텀 위젯 문법'),),

        // body: SizedBox(
        //   child: MyWidget(),
        // ),
        body: ListView(
          children: [
            hi,
            hi,
            hi,
          ],
        ),
      ),
    );
  }

}


// 커스텀 변수 정의
var hi = SizedBox(
  child: Text('Hello world!'),
);

// 커스텀 클래스 정의
class MyWidget extends StatelessWidget {
  const MyWidget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      child: Text('커스텀 위젯'),
    );
  }
}
