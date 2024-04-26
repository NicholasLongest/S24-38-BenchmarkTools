Attribute VB_Name = "Module1"
Sub Charts()

Dim ws As ActiveSheet
Dim ch As Chart
Dim dt As Range

Set dt = Range("E2", "E37")
Set ch = Shapes.AddChart2.Chart

ch.SetSourceData Source:=dt
ch.ChartType = xlLineStacked

ch.Parent.Activate
ActiveChart.Export ThisWorkbook.Path & "\test.jpg"
ch.Parent.Delete

ActiveSheet.Parent.Save
ActiveSheet.Parent.Close

End Sub

