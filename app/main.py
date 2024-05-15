from typing import Annotated
import xlwings as xw
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from mailjet import email_body
from lang_detect import detect_language_polyglot
import current_gpt as gpt

app = FastAPI()


def get_book(body: dict):
    """Dependency that returns the calling book and cleans it up again"""
    book = xw.Book(json=body)
    try:
        yield book
    finally:
        book.close()


# This is the type annotation that we're using in the endpoints
Book = Annotated[xw.Book, Depends(get_book)]


@app.post("/hello")
async def hello(book: Book):
    """If you're using FastAPI < 0.95.0, you have to replace the function signature
    like so: async def hello(book: xw.Book = Depends(get_book))
    """
    sheet = book.sheets[0]
    cell = sheet["A1"]
    if cell.value == "Hello xlwings!":
        cell.value = "Bye xlwings!"
    else:
        cell.value = "Hello xlwings!"

    # Return the following response
    return book.json()


@app.exception_handler(Exception)
async def exception_handler(request, exception):
    # This handles all exceptions, so you may want to make this more restrictive
    return PlainTextResponse(
        str(exception), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

@app.post("/generate")
async def generate(book: Book):
    sheet = book.sheets[0]

    # Start with the first row (row_num = 1)
    row_num = 2

    # Continue looping until there is no value in column A
    while True:
        cell_a = sheet.range(f"A{row_num}")  # Get the cell in column A

        # Check if the cell in column A is empty
        if cell_a.value:
            # Move to the next row
            row_num += 1
        else:
            row_num -= 1
            break
    
    #Get row values
    manager_name = sheet.range(f"B{row_num}").value
    guest_name = sheet.range(f"C{row_num}").value
    guest_email = sheet.range(f"D{row_num}").value
    observations = sheet.range(f"E{row_num}").value

    # Detect language
    detected_language, confidence = detect_language_polyglot(observations)
    print(f"Detected language: {detected_language} with confidence: {confidence:.2f}")

    #Generate review and title
    generated_review = gpt.generate_review(observations, detected_language)
    print("Review: ", generated_review)
    generated_title = gpt.generate_title(generated_review, detected_language)
    print("Title: ", generated_title)
    
    # Prepare and send email
    body = email_body(guest_name, manager_name, guest_email, detected_language, generated_review, generated_title)
    print("Email sent.")

    # Return the following response
    return book.json()





# Office Scripts and custom functions in Excel on the web require CORS
cors_app = CORSMiddleware(
    app=app,
    allow_origins="*",
    allow_methods=["POST"],
    allow_headers=["*"],
    allow_credentials=True,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:cors_app", host="127.0.0.1", port=8000, reload=True)
