import flet
import analyser
def capture(page: flet.Page):

    page.vertical_alignment=flet.MainAxisAlignment.CENTER
    page.horizontal_alignment=flet.CrossAxisAlignment.CENTER
    def result(e):
        if e.files:
            page.clean()
            analyser.analyse(page,e.files[0].path)         
    picker=flet.FilePicker(on_result=result)
    page.services.append(picker)
    page.add(flet.Text("Let's Start",size=40),flet.OutlinedButton("Select Image of Food Item",action=flet.PickFiles(picker,allow_multiple=False)))