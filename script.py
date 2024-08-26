from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import StreamingResponse
import qrcode
from io import BytesIO

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the QR Code Contact App!"}

@app.post("/generate-qrcode/")
async def generate_qrcode(phone_number: str = Form(...)):
    if not phone_number.isdigit() or len(phone_number) < 10:
        raise HTTPException(status_code=400, detail="Invalid phone number")

    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"tel: {phone_number}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code to a BytesIO stream
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Return the image as a StreamingResponse
    return StreamingResponse(img_io, media_type="image/png")

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
