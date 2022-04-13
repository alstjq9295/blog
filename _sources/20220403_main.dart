import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // 2022-04-02
  // @override
  // Widget build(BuildContext context) {
  //   return MaterialApp(
  //     home: Scaffold(
  //       appBar: AppBar(
  //         title: Text('Hello World!')
  //       ),
  //       body: Column(
  //         mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  //         crossAxisAlignment: CrossAxisAlignment.center,
  //         children: [
  //           Text('때릴꺼야?'),
  //           Icon(Icons.music_note),
  //           Image.asset('bonobono.jpg'),
  //         ]
  //       ),
  //       bottomNavigationBar: BottomAppBar(
  //         child: SizedBox( // Container 는 무거움
  //           height: 50,
  //           child: Row(
  //               mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  //               children: [
  //                 Icon(Icons.phone),
  //                 Icon(Icons.message),
  //                 Icon(Icons.contact_page)
  //               ]
  //           ),
  //         ),
  //       )
  //     )
  //   );
  // }

  // 2022-04-03
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar( title: Text('Hello World!!') ),

        // A type
        // body: Container(
        //   width: 350, height: 50, // color: Colors.green, # decoration 에 color 를 명시하기 때문에 중복사용 불가
        //   margin: EdgeInsets.all(20),
        //   padding: EdgeInsets.fromLTRB(10, 15, 15, 10), // (left, top, right, bottom)
        //   decoration: BoxDecoration(
        //     color: Colors.green,
        //     border: Border.all(color: Color(0xff42f2f5))
        //   ),
        //   child: Text('Good afternoon, good evening and goor night.'),
        // ),

        // B type
        body: Align(
          alignment: Alignment.center,
          child: Container(
            width: double.infinity, height: 200, color: Colors.green,
          ),
        ),
        bottomNavigationBar: BottomAppBar(
          child: SizedBox(
            height: 50,
            child: Row(
              mainAxisSize: MainAxisSize.max,
            ),
          ),
        ),
      ),
    );
  }

}
