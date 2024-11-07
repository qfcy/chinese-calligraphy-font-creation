Attribute VB_Name = "ģ��1"
Option Explicit

Sub ExportBitmaps()
    On Error Resume Next
    Dim s As Shape, doc As Document
    Dim exportPath As String, FileName_ As String
    Dim bitmapCount As Long
    Dim totalShapes As Long
    Dim expflt As ExportFilter

    ' ���õ���·��
    exportPath = "e:\����\" ' ���滻Ϊ���ĵ���·��
    totalShapes = 0
    bitmapCount = 0
    UserForm1.Show vbModeless
    
    For Each doc In Documents
        ' ���㵱ǰ�ĵ�������״��
        totalShapes = totalShapes + doc.ActivePage.Shapes.Count
    Next doc

    For Each doc In Documents
        ' ������ǰ�ĵ���������״
        For Each s In doc.ActivePage.Shapes
            If s.Type = cdrBitmapShape Then ' ����Ƿ�Ϊλͼ����
                ' ����λͼ
                FileName_ = "Bitmap_" & bitmapCount & "_" & Left(doc.Name, Len(doc.Name) - 4) & ".png" ' �ļ����а����ĵ������Ա����ͻ
                
                ' ����λͼ
                Set expflt = s.Bitmap.SaveAs(exportPath & FileName_, cdrPNG, cdrCompressionNone)
                
                ' ��ѡ��������������ѡ��
                With expflt
                    .Interlaced = True
                    .Transparency = 0
                    .InvertMask = False
                    .ColorIndex = 1
                    .Finish
                End With
                
                bitmapCount = bitmapCount + 1
                
                ' ���½�����
                UserForm1.Label1.Caption = "���ڵ���..." & bitmapCount & " / " & totalShapes & " (" & doc.FileName & ")"
                
                ' �ó��򱣳���Ӧ
                DoEvents
            End If
        Next s
    Next doc

    Unload UserForm1
    
    ' ��ʾ���
    'MsgBox bitmapCount & " λͼ������ɣ�"
End Sub
