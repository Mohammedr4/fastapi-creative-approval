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


The Rules I Chose

The brief asked for 2-3 rules from the policy docs. My thinking was to pick a few that would have a real impact and could be built reliably.

1. File Size Limit (10MB)

Source: Global Outdoor Copy Approval Guidelines

Justification: This was a technical requirement from their guidelines. If a file is too big for the ad servers, it's not going to work, so this is an immediate REJECT.

2. 16:9 Aspect Ratio

Source: Global Outdoor Copy Approval Guidelines

Justification: The same document mentioned 16:9 for digital screens. I check for this to catch distorted images, but I made it a REQUIRES_REVIEW since other formats might still be valid in some contexts.

3. Low Contrast

Source: ASA CAP Code (UK)

Justification: The ASA code talks a lot about clarity. To act as a proxy for legibility, I built a simple check to flag images that are "washed out." This also triggers a REQUIRES_REVIEW for a human to make the final call.

Design Decisions & Trade-offs

My main goal was to build a solution that respected the ~2 hour scope. That meant being practical from the start.

My core design decision was to keep the rules engine predictable. I focused on measurable rules from the documents, rather than trying to interpret vague concepts that would need ML. This approach keeps the service simple.

The main trade-off was with the contrast check. A truly accurate "legibility" detector is complex, so I chose a simple standard deviation heuristic. It's a pragmatic simplification that effectively flags the most obvious cases and keeps the service easy to maintain.

I decided to add an optional feature of metrics, as they make the API more professional. The /metrics endpoint is a simple way to monitor the service.

What I’d do next: The first thing I'd do is move the rule thresholds (e.g., LOW_CONTRAST_THRESHOLD) from hard-coded values into a config file or environment variables. That would make the service more flexible. After that, I would add structured logging for each decision.