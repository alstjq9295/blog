import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);
  
  // 2022-04-10
  // @override
  // Widget build(BuildContext context) {
  //   return MaterialApp(
  //     home: Scaffold(
  //       // appBar: AppBar( title: Text('광광우럭따') ),
  //       appBar: AppBar( actions: [Icon(Icons.list)], leading: Icon(Icons.home), title: Text('광광우럭따'), ),
  //       body: SizedBox(
  //         // child: Text('Hello World!', style: TextStyle(color: Color(0xff10e348)),),
  //
  //         // child: ElevatedButton(
  //         //     child: Text('부와악'),
  //         //     onPressed: (){},
  //         //     style: ButtonStyle()
  //         // ),
  //       ),
  //     )
  //   );
  // }

  // 2022-04-09 Homework
  // @override
  // Widget build(BuildContext context) {
  //   return MaterialApp(
  //       home: Scaffold(
  //         appBar: AppBar(
  //           title: Text('숙제', style: TextStyle(color: Colors.black),),
  //           leading: Icon(Icons.expand_more, color: Colors.black),
  //           actions: [
  //             IconButton(icon: Icon(Icons.search), color: Colors.black, onPressed: () {print('Searching for what?');}),
  //             IconButton(icon: Icon(Icons.list), color: Colors.black, onPressed: () {print('Listing for what?');}),
  //             IconButton(icon: Icon(Icons.notifications), color: Colors.black, onPressed: () {print('Searching for what?');}),
  //           ],
  //           backgroundColor: Colors.white,
  //         ),
  //         body: Container(
  //           width: double.infinity, height: 100, color: Colors.white,
  //           child: Row(
  //             // crossAxisAlignment: CrossAxisAlignment.start,
  //             // mainAxisAlignment: MainAxisAlignment.spaceEvenly,
  //             children: [
  //               Image.asset('bonobono.jpg'),
  //               Column(
  //                 crossAxisAlignment: CrossAxisAlignment.start,
  //                 children: [
  //                   Text('모르는게 아니야. 알 때까지 시간이 좀 걸리는거야', style: TextStyle(fontSize: 15), ),
  //                   Text('너부리야', style: TextStyle(fontSize: 8), ),
  //                   Text('헛소리하지마 임마', style: TextStyle(fontSize: 10), ),
  //                   IconButton(icon: Icon(Icons.favorite_outline), onPressed: () {print('때릴꺼야?');})
  //                 ],
  //               )
  //             ],
  //           ),
  //         )
  //       )
  //   );
  // }

  // 2022-04-09 5th lecture
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('금호동3가', style: TextStyle(color: Colors.black),),
          leading: Icon(Icons.expand_more, color: Colors.black),
          actions: [
            IconButton(icon: Icon(Icons.search), color: Colors.black, onPressed: () {print('Searching for what?');}),
            IconButton(icon: Icon(Icons.list), color: Colors.black, onPressed: () {print('Listing for what?');}),
            IconButton(icon: Icon(Icons.notifications), color: Colors.black, onPressed: () {print('Searching for what?');}),
          ],
          backgroundColor: Colors.white,
        ),

        // body: Row(
        //   children: [
        //     Flexible(child: Container(color: Colors.red,), flex: 3,),
        //     Flexible(child: Container(color: Colors.blue,), flex: 7,),
        //     Expanded(child: Container(color: Colors.black,))
        //   ],
        // ),

        body: Container(
          height: 150,
          padding: EdgeInsets.all(10),
          child: Row(
            children: [
              Image.asset('bonobono.jpg', width: 70),
              SizedBox(
                width: 350,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text('모르는게 아니야. 알 때까지 시간이 좀 걸리는거야', style: TextStyle(fontSize: 15), ),
                    Text('너부리야', style: TextStyle(fontSize: 8), ),
                    Text('헛소리하지마 임마', style: TextStyle(fontSize: 10), ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        IconButton(icon: Icon(Icons.favorite_outline), onPressed: () {print('때릴꺼야?');}),
                        Text('4')
                      ],
                    )
                  ],
                ),
              )
            ],
          ),
        ),
      )
    );
  }

}
