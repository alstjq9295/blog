import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // 2022-04-10 homework of 6th lecture
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
          appBar: AppBar(),
          body: ListView(
            children: [
              Column(
                children: [
                  Row(
                    children: [
                      Icon(Icons.account_circle),
                      Text('너부리')
                    ],
                  ),
                  Row(
                    children: [
                      Icon(Icons.account_circle),
                      Text('보노보노')
                    ],
                  ),
                  Row(
                    children: [
                      Icon(Icons.account_circle),
                      Text('포로리')
                    ],
                  )
                ],
              )
            ],
          ),
          bottomNavigationBar: CustomBottomBar(),
        )
    );
  }
}


class CustomBottomBar extends StatelessWidget {
  const CustomBottomBar({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BottomAppBar(
      child: SizedBox(
        height: 50,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            Icon(Icons.phone),
            Icon(Icons.message),
            Icon(Icons.contact_page)
          ]
        ),
      ),
    );
  }
}
