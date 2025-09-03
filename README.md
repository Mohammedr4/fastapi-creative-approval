Creative Approval API

Here's a small FastAPI service I built for a technical take-home task. It's a simple API that takes an image upload and checks it against a few advertising rules.

Running Locally:

You'll need Python 3.11+ to run this on your machine.

1. Clone the project and cd into the folder.
2. Set up a virtual environment:

On Windows:

python -m venv venv
.\venv\Scripts\activate

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate

3. Install dependencies:

pip install -r requirements.txt

4. Start the server:

uvicorn src.main:app --reload

You can now access the API at http://127.0.0.1:8000. The interactive documentation, which you can use to test the endpoints, is at http://127.0.0.1:8000/docs.

Running with Docker:

If you have Docker Desktop running, you can get started with two commands:

1. Build the image:

docker build -t creative-approval-service .

2. Run the container:

docker run -p 8000:8000 creative-approval-service


How to Run the Tests

I used pytest for the automated tests. Once you've set it up locally, just run this command from the main project folder:

pytest


The Rules I Implemented

The brief asked me to choose 2-3 rules from the policy docs. I went with these because they seemed like the most practical and impactful checks I could build reliably.

1. File Size Limit (10MB):
This was a hard technical requirement from the Global Outdoor guidelines. If a file is too big for their ad servers, it's an automatic REJECT.

2. 16:9 Aspect Ratio:
The same document mentioned 16:9 for digital screens. I check for this to catch distorted images, but I made it a REQUIRES_REVIEW since other formats might still be okay in some cases.

3. Low Contrast:
To act as a proxy for legibility (from the ASA code), I built a simple check to flag images that are low-contrast or "washed out." This also triggers a REQUIRES_REVIEW.


My Design Choices

My main goal was to build a solid, well-tested solution that fit the ~2 hour scope. This meant making some pragmatic choices.
- Simplifications:
My contrast check uses a simple standard deviation calculation. It's a quick and effective way to get a result without adding heavy dependencies or complex image analysis. It gets the job done.

- Optional Features:
I decided to add the optional features because they make the project feel more complete. The improved OpenAPI docs make the API easier to use, and the /metrics endpoint is a good first step towards real-world monitoring.

- If I Had More Time:
The first thing I'd do is move the rule thresholds (like the contrast value) into a config file or environment variables so they aren't hard-coded. After that, I would add structured logging for every decision the API makes.