local Make = import '../sonnet/constructors.libsonnet';

Make.Workbook('Empty', [
  Make.Sheet('Alice', []),
  Make.Sheet('Bob', []),
])
