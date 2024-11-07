Attribute VB_Name = "模块1"
Option Explicit

Sub ExportBitmaps()
    On Error Resume Next
    Dim s As Shape, doc As Document
    Dim exportPath As String, FileName_ As String
    Dim bitmapCount As Long
    Dim totalShapes As Long
    Dim expflt As ExportFilter

    ' 设置导出路径
    exportPath = "e:\导出\" ' 请替换为您的导出路径
    totalShapes = 0
    bitmapCount = 0
    UserForm1.Show vbModeless
    
    For Each doc In Documents
        ' 计算当前文档的总形状数
        totalShapes = totalShapes + doc.ActivePage.Shapes.Count
    Next doc

    For Each doc In Documents
        ' 遍历当前文档的所有形状
        For Each s In doc.ActivePage.Shapes
            If s.Type = cdrBitmapShape Then ' 检查是否为位图对象
                ' 导出位图
                FileName_ = "Bitmap_" & bitmapCount & "_" & Left(doc.Name, Len(doc.Name) - 4) & ".png" ' 文件名中包含文档名称以避免冲突
                
                ' 保存位图
                Set expflt = s.Bitmap.SaveAs(exportPath & FileName_, cdrPNG, cdrCompressionNone)
                
                ' 可选：设置其他导出选项
                With expflt
                    .Interlaced = True
                    .Transparency = 0
                    .InvertMask = False
                    .ColorIndex = 1
                    .Finish
                End With
                
                bitmapCount = bitmapCount + 1
                
                ' 更新进度条
                UserForm1.Label1.Caption = "正在导出..." & bitmapCount & " / " & totalShapes & " (" & doc.FileName & ")"
                
                ' 让程序保持响应
                DoEvents
            End If
        Next s
    Next doc

    Unload UserForm1
    
    ' 提示完成
    'MsgBox bitmapCount & " 位图导出完成！"
End Sub
