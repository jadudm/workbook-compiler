local C = import '../fixtures/lib/constructors.libsonnet';

C.Workbook(
  'Empty workbook',
  [
    C.Sheet(
      'First Sheet',
      [
        C.LinearRange('numbers',
                      C.Cell('RC', 1, 1),
                      3,
                      contents=[
                        C.Contents(3),
                        C.Contents(5),
                        C.Contents(8),
                      ],),
      ],
    ),
  ],
)
