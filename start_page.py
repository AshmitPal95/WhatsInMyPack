import flet
import check_internet
import asyncio

async def wait(page):
    await asyncio.sleep(2)
    page.clean()
    check_internet.main(page)

def main(page: flet.Page):
    page.vertical_alignment=flet.MainAxisAlignment.CENTER
    page.horizontal_alignment=flet.CrossAxisAlignment.CENTER
    page.add(flet.Image("assets/app_icon_image.png",width=200,height=200),flet.Text("What's In My Pack",size=40),flet.ProgressRing(width=50,height=50),flet.Text("Powered by Google Gemini",color="grey"))
    page.update()

    page.run_task(wait,page)
    
flet.run(main)
