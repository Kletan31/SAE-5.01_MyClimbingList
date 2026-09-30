import 'package:flutter_test/flutter_test.dart';
import 'package:my_climbing_list_poc/main.dart';

void main() {
  testWidgets('application starts', (tester) async {
    await tester.pumpWidget(const MyClimbingListApp());
    expect(find.text('My Climbing List'), findsOneWidget);
  });
}
