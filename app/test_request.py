import requests

url = "http://localhost:8000/api/reply"
payload = {
    "platform": "instagram",
    "post_text": """
 	
I gain 100-200 followers a day 👇

People pay thousands of dollars for this strategy.

✅ Don't forget to SAVE this and 10x your growth.

You wouldn't want to LOSE it 😨

Stop complaining about low reach, no engagement and slow growth.

Everything you need to grow on Instagram is in your control.

✨ Remember to check your insights every week, and double down on what works.

✨ Keep posting consistently for 120-180 days to see results.

✨ Have patience. Trust the process, and don't get attached to the results.

Follow to become an authority on Instagram:

@akilasocial
@akilasocial
.""",
    "context": "",
    "include_analysis": True
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Reply generated successfully:")
    print(response.json())
else:
    print(f"Failed to generate reply: {response.status_code}")
    print(response.json())