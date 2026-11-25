import flet
import socket

def check_connection():
    try:
        with socket.create_connection(("8.8.8.8",53), timeout=3):
            return True
    except OSError:
        return False



def main(page: flet.Page):

    def retry(e):
        page.clean()
        main(page)

    page.vertical_alignment = flet.MainAxisAlignment.CENTER
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER

    if check_connection():
        import capture_photo
        capture_photo.capture(page)

    else:
        page.add(
            flet.Image(src="assets/no_internet_image.png",width=200,height=200),
            flet.Text("No Internet. Try reconnecting"),
            flet.OutlinedButton("Retry",on_click=retry))
    