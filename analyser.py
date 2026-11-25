import flet
from config import gemini_client
import json

def analyse(page: flet.Page,image_path):
    page.vertical_alignment=flet.MainAxisAlignment.CENTER
    page.horizontal_alignment=flet.CrossAxisAlignment.CENTER
    spinner=flet.ProgressRing(width=50,height=50)
    error_text=flet.Text("",color="red",visible=False)
    page.add(spinner,error_text)
    page.update()
    client=gemini_client()
    try:
            uploaded_image=client.files.upload(file=image_path)
            response=client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    uploaded_image,
                    """
                    Analyze the image of the given packaged food item and return its complete nutrition label,
                    list of harmful ingredients,
                    a grade based on the Nutri-Score grading system implemented in Germany,
                    and a one line summary of its nutritional value.
                    Prefer nutrition values per 100g or 100ml if available on the package.
                    If any information is not available, return "N/A" instead of guessing.
                    Return only valid JSON
                    Do not include markdown.
                    Do not include explanations.
                    Do not include code fences.
                    Do not include any text before or after the JSON.
                    JSON format:
                    {
                        "Serving Size":"",
                        "Energy(kcal)":"",
                        "Protein(grams)":"",
                        "Carbohydrate(grams)":"",
                        "Added Sugar(grams)":"",
                        "Total Sugar(grams)":"",
                        "Saturated Fat(grams)":"",
                        "Trans Fat(grams)":"",
                        "Total Fat(grams)":"",
                        "Fiber(grams)":"",
                        "Sodium(milligrams)":"",
                        "Ingredients":[],
                        "Harmful ingredients":[],
                        "One Line Overview":"",
                        "Grade":""
                    }
                    """
                ]
            )
    except Exception as ex:
        print("ERROR:",ex) #Developer testing for unexpected errors.
        if spinner in page.controls:
           page.controls.remove(spinner)       
        error_text.value="Unable to connect to fetch results at the moment.\nPlease try again later."
        if "503" in str(ex):
            error_text.value="Google Gemini is currently facing high demand.\nTry again later."
        else:
            error_text.value=str(ex)
        error_text.visible=True
        page.update()
        return 
    try:
        output=json.loads(response.text)
        if not isinstance(output,dict):
             if spinner in page.controls:
                page.controls.remove(spinner)
             error_text.value="Unexpected response format\nPlease try again later."
             error_text.visible= True
             page.update()
             return
        if not output:
             if spinner in page.controls:
                  page.controls.remove(spinner)
             error_text.value="No nutritional information found"
             error_text.visible = True
             page.update()
             return
    except json.JSONDecodeError:
         print("RAW RESPONSE:") #Developer Testing for correct JSON formatting.
         print(response.text)
         if spinner in page.controls:
            page.controls.remove(spinner)
         error_text.value="Unable to process results.\nPlease try again later."
         error_text.visible= True
         page.update()
         return
    error_text.visible=False
    page.update()
    rows=[]
    for key,value in output.items():
            if isinstance(value,list):
                value = ", ".join(value)
            rows.append(flet.DataRow(cells=[
                flet.DataCell(flet.Text(str(key))),
                flet.DataCell(flet.Text(str(value)))
            ]))
    output_table=flet.DataTable(
            columns=[
                 flet.DataColumn(flet.Text("Field")),
                 flet.DataColumn(flet.Text("Value"))
            ],
            rows=rows)
    grade = output.get("Grade", "N/A")
    warning_message=flet.Text("Warning:Some information may be outdated or incorrect. Please verify before use.",color="orange")
    if spinner in page.controls:
         page.controls.remove(spinner)
    page.add(flet.Text(f"Nutri-Score Grade:{grade}",size=20),output_table,warning_message)
    page.update()
        

