from openai import OpenAI
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv 



load_dotenv()

# Make sure API key is defined
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Helper: encode image to base64
def encode_image_to_base64(image):
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Helper: extract text from one image
def extract_text_from_image(image):
    image_data = encode_image_to_base64(image)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts text from images."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                    }
                ],
            },
        ],
        temperature=0.2,
        max_tokens=2000
    )

    return response.choices[0].message.content.strip()

# 🔥 Final Function: extract text from multiple images and save
def extract_and_save_text_from_images(images, output_file="extracted_text.txt"):
    all_text = ""

    for i, image in enumerate(images):
        try:
            print(f"📄 Processing image {i+1} of {len(images)}...")
            extracted = extract_text_from_image(image)
            all_text += f"\n\n--- Text from Image {i+1} ---\n{extracted}"
        except Exception as e:
            print(f"❌ Error processing image {i+1}: {e}")

    # Save combined text to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_text)

    print(f"✅ Text extracted and saved to {output_file}")
    return output_file